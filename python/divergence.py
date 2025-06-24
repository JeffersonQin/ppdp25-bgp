from cvc5.pythonic import *
import maude

from gadget import Gadget
from hook import CheckRepetitionHook
from metarouting import *

import os
import pathlib
import tempfile
import sys


def get_sp_links(solver: Solver):
    set_links = set()

    for uc in solver.unsat_core():
        str_uc = str(uc)
        if str_uc.startswith("Score"):
            str_uc = str_uc.replace("(", "").replace(")", "").replace("Rank", "").replace("Concat", "").replace("Unit", "").replace("Score", "")
            str_uc = str_uc.replace("|", "").replace("Node", "").replace("\n", "").replace(" ", "")
            str_uc = str_uc[:str_uc.find("=")].strip()
            list_uc = str_uc.split(",")
            
            for i in range(len(list_uc)-2):
                edge = list_uc[i], list_uc[i+1]


                if edge not in set_links:
                    set_links.add(edge)

                break


    return set_links


def maude_search(gadget : Gadget, sp_links : set, sp_recur_size : int, shared_data):
    str_nodes = [str(node) for node in gadget.nodes]
    convert_node = lambda node : f"nid({str_nodes.index(str(node))})"
    convert_links = lambda links : f"{', '.join([f'({convert_node(n2)} => {convert_node(n1)})' for n1, n2 in links])}"

    curr_file_dir = pathlib.Path(__file__).parent.resolve()
    load_file = (curr_file_dir.parent / "maude" / "spvp.maude")

    maude_str = gadget_to_maude(gadget).replace("__SP_LINKS_REPLACE__", convert_links(sp_links)).replace("__SP_RECUR_SIZE_REPLACE__", str(sp_recur_size))
    no_sol_phrase = "No solution."

    old_stdout_fd = os.dup(1)
    old_stderr_fd = os.dup(2)


    with tempfile.TemporaryFile(mode='w+b') as tmp:
        os.dup2(tmp.fileno(), 1)
        os.dup2(tmp.fileno(), 2) 

        maude.init()
        maude.load(str(load_file))
        check_repetition_hook = CheckRepetitionHook()
        maude.connectEqHook("$check-repetition", check_repetition_hook)
        maude.input(maude_str)

        sys.stdout.flush()
        sys.stderr.flush()

        tmp.seek(0)
        output = tmp.read().decode()
        output_len = len(output)

        if no_sol_phrase in output:
            os.dup2(old_stdout_fd, 1) 
            os.dup2(old_stderr_fd, 2) 

            os.close(old_stdout_fd) 
            os.close(old_stderr_fd)
            print(f"No Solution for recur size {sp_recur_size}.")
            print(output)
            exit(1)

        lines = output.splitlines()

        
        try:
            sol_line = lines[4]
            sol_num = sol_line.replace("Solution 1 (state ", "").replace(")", "")
        except Exception as e:
            os.dup2(old_stdout_fd, 1) 
            os.dup2(old_stderr_fd, 2) 

            os.close(old_stdout_fd) 
            os.close(old_stderr_fd)
            print("Error parsing solution")
            print(len(lines))
            print(output)
            for line in lines:
                print(line, flush=True)
            print(e, flush=True)
            exit(2)

        
        
        maude_exec_show_path = f"show path {sol_num} ."
        maude.input(maude_exec_show_path)
        tmp.seek(output_len)
        output2 = tmp.read().decode()
        

        os.dup2(old_stdout_fd, 1)  
        os.dup2(old_stderr_fd, 2)  

        os.close(old_stdout_fd) 
        os.close(old_stderr_fd)

        shared_data.append((sp_recur_size, output, output2))

    exit(0)




def gadget_to_maude(gadget : Gadget, sp_links : set = None, sp_recur_size : int = None, out_file=None, name="GADGET-DIVERGENCE"):
    str_nodes = [str(node) for node in gadget.nodes]
    convert_node = lambda node : f"nid({str_nodes.index(str(node))})"
    convert_path = lambda path : f"({' '.join([convert_node(node) for node in path])})"
    convert_pref = lambda pref : f" :: ".join([convert_path(path) for path in pref])
    convert_ns = lambda ns : f", ".join([convert_node(node) for node in ns])

    convert_links = lambda links : f"{', '.join([f'({convert_node(n2)} => {convert_node(n1)})' for n1, n2 in links])}"
    
   
    node_oids = [f"N{i}" for i in range(len(gadget.nodes))]
    node_oids_str = " ".join(node_oids)
    node_permitted_decl = [f"PT{i}" for i in range(len(gadget.nodes))[1:]]
    node_permitted_decl_str = " ".join(node_permitted_decl)
    node_permitted_def = [f"eq {pt} = {convert_pref(pref)} ." for pt, pref in zip(node_permitted_decl, list(gadget.paths.values())[1:], strict=True)]
    node_permitted_def_str = "\n".join(node_permitted_def)
    node_neighbors_decl = [f"NS{i}" for i in range(len(gadget.nodes))]
    node_neighbors_decl_str = " ".join(node_neighbors_decl)
    node_neighbors_def = [f"eq {ns} = {convert_ns(adj)} ." for ns, adj in zip(node_neighbors_decl, gadget.adj.values(), strict=True)]
    node_neighbors_def_str = "\n".join(node_neighbors_def)


    node_classes = [f"< N0 : NodeClass | id : nid(0), rib : nullPath, rib-in : emptyLPM, permitted : nilPL, neighbours : emptyNodes, queue : emptyLQM >"]

    for i, node in enumerate(gadget.nodes[1:], start=1):
        node_class = f"< N{i} : NodeClass | id : nid({i}), rib : nullPath, rib-in : emptyLPM, permitted : PT{i}, neighbours : NS{i}, queue : emptyLQM >"
        node_classes.append(node_class)

    node_classes_str = "\n".join(node_classes)


    gadget_module_str = \
f"""\
mod {name} is

  inc SPVP .

  ops {node_oids_str} : -> Oid .

  --- preference table does not include node itself
  ops {node_permitted_decl_str} : -> PathList .
  {node_permitted_def_str}

  --- neighbours should not include destination
  ops {node_neighbors_decl_str} : -> Nodes .
  {node_neighbors_def_str}

  op path-to-origin : -> Path .
  eq path-to-origin = (nid(0)) .

  eq sp-links = {convert_links(sp_links) if sp_links is not None else "__SP_LINKS_REPLACE__"} .
  eq sp-recur-size = {sp_recur_size if sp_recur_size is not None else "__SP_RECUR_SIZE_REPLACE__"} .

  op gadget : -> Configuration .
  eq gadget =
    broadcast path-to-origin from nid(0) to NS0 in (
      {node_classes_str}
    ) .

  op dpc : -> Configuration .
  eq dpc = dpo-clear(sys-new: gadget < DPC : DPClass | 
      consume : nilLPL,
      produce : nilNPL,
      init : emptyLQM,
      all-rib : nilRTL,
      all-rib-in : nilLPML,
      sz : 0 > ) .

  op gadget-system : -> BGP .
  eq gadget-system = {{ dpc gadget }} . 
  

endm


search [1] in {name} : gadget-system =>+ {{ diverged C:Configuration }} .



"""
    
    return gadget_module_str


