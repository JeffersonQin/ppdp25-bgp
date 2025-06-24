from cvc5.pythonic import *

class Gadget:

    def __init__(self, name, adj_map, path_map, origin=None, edge_delim="#"):
        self.name = name
        self.nodes = list(path_map.keys())
        self.adj = adj_map
        self.paths = {k : [tuple(p) for p in v] for k, v in path_map.items()}
        self.origin = self.nodes[0] if origin is None else origin
        self.origin_path = tuple([self.origin])
        self.edge_delim = edge_delim

        self.cache_create_path = dict()
        self.cache_create_queue = dict()

        self.num_nodes = len(self.nodes)

        self.edges = []
        for n, adj_list in self.adj.items():
            if n == self.origin:
                self.edges.extend([(a, n) for a in adj_list])
            else:
                self.edges.extend([(n, a) for a in adj_list])

        self.num_edges = len(self.edges)
        self.num_paths = sum([len(pref_list) for pref_list in self.paths.values()])

    