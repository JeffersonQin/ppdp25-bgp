from gadget import Gadget
from operators import *
from spp import *
from workflow import work_single

TIMEOUT = 1 * 60 * 60 # one hour

GOOD_GADGET = create_good_gadget()
NAUGHTY_GADGET = create_naughty_gadget()
DISAGREE_GADGET = create_disagree_gadget()


RECUR_SIZE_MAP = {
    GOOD_GADGET : 0,
    NAUGHTY_GADGET : 4,
    DISAGREE_GADGET : 4,
}

EXPECT_RESULT_MAP = {
    GOOD_GADGET : "CONVERGE",
    NAUGHTY_GADGET : "DIVERGE",
    DISAGREE_GADGET : "DIVERGE",
}

ACTUAL_RESULT_MAP = {
    True : "CONVERGE",
    False : "DIVERGE",
    None : "TIMEOUT",
    }




def run_base_experiment(gadget : Gadget):
    name = gadget.name
    sp_recur_size = RECUR_SIZE_MAP[gadget]
    expected_result = EXPECT_RESULT_MAP[gadget]
    num_nodes = gadget.num_nodes
    num_edges = gadget.num_edges
    num_paths = gadget.num_paths

    result, sp_links, _, smt_time, maude_time = work_single(gadget, sp_recur_size, timeout=TIMEOUT)
    
    actual_result = ACTUAL_RESULT_MAP[result]

    print(f"Name: {name}")
    print(f"Expected Result: {expected_result}" )
    print(f"Actual Result: {actual_result}" )
    print(f"Number of Nodes: {num_nodes}" )
    print(f"Number of Links: {num_edges}" )
    print(f"Number of Paths: {num_paths}" )
    print(f"Time For SMT: {smt_time} seconds" )
    print(f"Time for Maude: {maude_time} seconds" )
    print(f"sp_recur_size: {sp_recur_size}" )
    print(f"sp_links: {sp_links}" )
    print()


def run_rooted_experiment(*gadgets : Gadget):
    test_gadget = gadgets[-1]

    rooted_gadget = create_rooted_gadget(*gadgets)

    name = f"Rooted Gadget {test_gadget.name} with size {len(gadgets)}"
    sp_recur_size = RECUR_SIZE_MAP[test_gadget]
    expected_result = EXPECT_RESULT_MAP[test_gadget]
    num_nodes = rooted_gadget.num_nodes
    num_edges = rooted_gadget.num_edges
    num_paths = rooted_gadget.num_paths

    result, sp_links, _, smt_time, maude_time = work_single(rooted_gadget, sp_recur_size, timeout=TIMEOUT)
    
    actual_result = ACTUAL_RESULT_MAP[result]

    print(f"Name: {name}")
    print(f"Expected Result: {expected_result}" )
    print(f"Actual Result: {actual_result}" )
    print(f"Number of Nodes: {num_nodes}" )
    print(f"Number of Links: {num_edges}" )
    print(f"Number of Paths: {num_paths}" )
    print(f"Time For SMT: {smt_time} seconds" )
    print(f"Time for Maude: {maude_time} seconds" )
    print(f"sp_recur_size: {sp_recur_size}" )
    print(f"sp_links: {sp_links}" )
    print()


def run_nested_experiment(*gadgets : Gadget):
    test_gadget = gadgets[0]

    nested_gadget = create_chain_nested_gadgets(*gadgets)

    name = f"Nested Gadget {test_gadget.name} with size {len(gadgets)}"
    sp_recur_size = RECUR_SIZE_MAP[test_gadget]
    expected_result = EXPECT_RESULT_MAP[test_gadget]
    num_nodes = nested_gadget.num_nodes
    num_edges = nested_gadget.num_edges
    num_paths = nested_gadget.num_paths

    result, sp_links, _, smt_time, maude_time = work_single(nested_gadget, sp_recur_size, timeout=TIMEOUT)
    
    actual_result = ACTUAL_RESULT_MAP[result]

    print(f"Name: {name}")
    print(f"Expected Result: {expected_result}" )
    print(f"Actual Result: {actual_result}" )
    print(f"Number of Nodes: {num_nodes}" )
    print(f"Number of Links: {num_edges}" )
    print(f"Number of Paths: {num_paths}" )
    print(f"Time For SMT: {smt_time} seconds" )
    print(f"Time for Maude: {maude_time} seconds" )
    print(f"sp_recur_size: {sp_recur_size}" )
    print(f"sp_links: {sp_links}" )
    print()