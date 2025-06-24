from gadget import Gadget 

def create_rooted_gadget(*args : Gadget):
    num_gadgets = len(args)
    rooted_origin = "0"
    rooted_adj = {rooted_origin : []}
    rooted_paths = {rooted_origin : []}
    rooted_name = f"Rooted Gadget with {num_gadgets} gadgets created from: {['; '.join(g.name for g in args)]}"
    delim = "_"

    for i, gadget in enumerate(args, start=1):
        for j, node in enumerate(gadget.nodes):
            new_node = f"{i}{delim}{j}"
            rooted_adj[new_node] = [f"{i}{delim}{gadget.nodes.index(a)}" for a in gadget.adj[node]]
            rooted_paths[new_node] = [[f"{i}{delim}{gadget.nodes.index(n)}" for n in path] + [rooted_origin] for path in gadget.paths[node]]


            if node == gadget.origin:
                rooted_adj[rooted_origin].append(new_node)
                rooted_paths[new_node].append((rooted_origin,))



    return Gadget(rooted_name, rooted_adj, rooted_paths)


def create_nested_gadgets(gadget1 : Gadget, gadget2 : Gadget):
    nested_origin = "0"
    nested_name = f"({gadget1.name}) NESTED WITH ({gadget2.name})"
    nested_adj = {nested_origin : []}
    nested_paths = {nested_origin : []}
    delim = "_"


    for i, n1 in enumerate(gadget1.nodes):
        if n1 == gadget1.origin:
            continue


        nested_paths[f"{gadget1.nodes.index(n1)}{delim}{0}"] = []
        for p1 in gadget1.paths[n1]:

            op = tuple([f"{gadget1.nodes.index(node)}{delim}{0}" for node in p1[:-1]] + [nested_origin])

            if op not in nested_paths[f"{gadget1.nodes.index(n1)}{delim}{0}"]:
                nested_paths[f"{gadget1.nodes.index(n1)}{delim}{0}"].append(op)

        for j, n2 in enumerate(gadget2.nodes):
            new_node = f"{i}{delim}{j}"   

            if n2 == gadget2.origin:
                nested_adj[new_node] = [nested_origin] + [f"{i}{delim}{gadget2.nodes.index(k)}" for k in gadget2.adj[n2]] + [f"{gadget1.nodes.index(k)}{delim}{0}" for k in gadget1.adj[n1] if k != gadget1.origin]
                nested_adj[nested_origin].append(new_node)
                continue

            nested_adj[new_node] =  ([f"{i}{delim}{0}"] if n2 in gadget2.adj[gadget2.origin] else []) + [f"{i}{delim}{gadget2.nodes.index(k)}" for k in gadget2.adj[n2]]
            nested_paths[new_node] = [] 


            for p1 in gadget1.paths[n1]:
                for p2 in gadget2.paths[n2]:
                    np1 = tuple([f"{i}{delim}{gadget2.nodes.index(node)}" for node in p2] + [f"{gadget1.nodes.index(node)}{delim}{0}" for node in p1[:-1]] + [nested_origin])
                    np2 = tuple([f"{i}{delim}{gadget2.nodes.index(node)}" for node in p2] + [nested_origin])
                    

                    if np1 not in nested_paths[new_node]:
                        nested_paths[new_node].append(np1)

                    if np2 not in nested_paths[new_node]:
                        nested_paths[new_node].append(np2)


    return Gadget(nested_name, nested_adj, nested_paths)

                             
def create_chain_nested_gadgets(*gadgets):
    if len(gadgets) == 0:
        return None
    
    if len(gadgets) == 1:
        return gadgets[0]
    

    if len(gadgets) == 2:
        return create_nested_gadgets(gadgets[0], gadgets[1])
    

    temp_gadget = gadgets[0]
    for g in gadgets[1:]:
        temp_gadget = create_nested_gadgets(temp_gadget, g)

    
    return temp_gadget
    



            


            










    









