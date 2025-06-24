from gadget import *

DEFAULT_EDGE_DELIM = "#"

def create_good_gadget():
    good_name = "GOOD GADGET"
    good_adj_map = {
        0: [1, 2, 3],
        1: [2, 3],
        2: [1, 4],
        3: [1, 4],
        4: [2, 3],
    }
    good_paths_map = {
        0 : [],
        1 : [[3, 0], [0]],
        2 : [[1, 0], [0]],
        3 : [[0]], 
        4 : [[3, 0], [2, 0]]  
    }


    return Gadget(good_name, good_adj_map, good_paths_map, edge_delim=DEFAULT_EDGE_DELIM)

def create_bad_gadget():
    bad_name = "BAD GADGET"
    bad_adj_map = {
        0 : [1, 2, 3],
        1 : [2, 3],
        2 : [1, 4],
        3 : [1, 4],
        4 : [2, 3],
    }
    bad_paths_map = {
        0 : [],
        1 : [[3, 0], [0]],
        2 : [[1, 0], [0]],
        3 : [[4, 2, 0], [0]], 
        4 : [[2, 0], [3, 0]], 
    }


    return Gadget(bad_name, bad_adj_map, bad_paths_map, edge_delim=DEFAULT_EDGE_DELIM)


def create_naughty_gadget():
    naughty_name = "NAUGHTY GADGET"
    naughty_adj_map = {
        0 : [1, 2, 3],
        1 : [2, 3],
        2 : [1, 4],
        3 : [1, 4],
        4 : [2, 3],
    }
    naughty_paths = {
        0 : [],
        1 : [[3, 0], [0]],
        2 : [[1, 0], [0]],
        3 : [[4, 2, 0], [0]], 
        4 : [[3, 0], [2, 0]], 
    }
    return Gadget(naughty_name, naughty_adj_map, naughty_paths, edge_delim=DEFAULT_EDGE_DELIM)



def create_disagree_gadget():
    disagree_name = "DISAGREE GADGET"
    disagree_adj_map = {
        0 : [1, 2],
        1 : [2],
        2 : [1],

    }
    disagree_paths_map = {
        0 : [],
        1 : [[2, 0], [0,]],
        2 : [[1, 0], [0,]],

    }

    return Gadget(disagree_name, disagree_adj_map, disagree_paths_map, edge_delim=DEFAULT_EDGE_DELIM)
