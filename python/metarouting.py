from gadget import Gadget 

from cvc5.pythonic import *

# returns (r, solver) where r in [SAT, UNSAT, UNKNOWN]
def check_convergence(g : Gadget):
    nodes = g.nodes
    edges = g.edges
    paths = g.paths
    origin = g.origin

    

    # START SYMBOLIC DECL
    Node = Datatype("Node")
    num_nodes = len(nodes)

    for node in nodes:
        Node.declare(f"Node({node})")

    node_sort = Node.create()
    smt_nodes = [node_sort.constructor(i)() for i in range(num_nodes)]


    node_dict = dict()
    for n, sn in zip(nodes, smt_nodes, strict=True):
        node_dict[n] = sn

    # Create smt sort for edges in a gadget
    Edge = Datatype("Edge")
    num_edges = len(g.edges)

    for a, b in g.edges:
        Edge.declare(f"{a}{g.edge_delim}{b}")

    edge_sort = Edge.create()
    smt_edges = [edge_sort.constructor(i)() for i in range(num_edges)]

    edge_dict = dict()
    for e, se in zip(g.edges, smt_edges, strict=True):
        edge_dict[e] = se


    CACHE_CREATE_PATH = dict()


    def create_path(*path):
        p = tuple(*path)

        if p in CACHE_CREATE_PATH:
            return CACHE_CREATE_PATH[p]

        if len(p) == 0:
            CACHE_CREATE_PATH[p] = empty_path
            return empty_path
        
        if len(p) == 1:
            result = Unit(node_dict[p[0]])
            CACHE_CREATE_PATH[p] = result
            return result
        
        result = Concat([Unit(node_dict[p[i]]) for i in range(len(p))])
        CACHE_CREATE_PATH[p] = result
        return result


    path_sort = SeqSort(node_sort)
    empty_path = Empty(path_sort)

    smt_paths = []
    for k, v in g.paths.items():
        for path in v:
            smt_paths.append(create_path((k,) + path))


    # Helper functions to create relevant smt symbols
    Path = lambda idx, prefix="" : Const(f"{prefix}Path({idx})", path_sort)
    Score = lambda path : Function("Score", path_sort, IntSort())(path)

    score_formulas = [Score(empty_path) == 0]

    for node, pathlist in g.paths.items():
        for s, path in enumerate(reversed(pathlist)):
            score_formulas.append(Score(create_path((node,) + path)) == s+1)

    # END SYMBOLCI DECL

    nodes = g.nodes
    origin = g.origin

    SeqTail = lambda p : SubSeq(p, 1, Length(p)-1)
    Rank = Function("Rank", path_sort, IntSort())

    formulas = [
        *score_formulas,

        *[
            Path(i) == sp for i, sp in enumerate(smt_paths)
        ],

       *[
            Rank(p) >= 0
            for p in smt_paths
        ],

        *[
            Implies(
                p1 != p2,
                Rank(p1) != Rank(p2)
            )
            for p1 in smt_paths for p2 in smt_paths
        ],

        *[
            Implies(
                And(p1[0] == p2[0], Score(p1) < Score(p2)),
                Rank(p1) > Rank(p2)
            )
            for p1 in smt_paths for p2 in smt_paths
        ],

        *[
            Implies(
                SeqTail(p1) == p2,
                Rank(p1) > Rank(p2))
                for p1 in smt_paths for p2 in smt_paths
        ],
    ]

    solver = Solver() 
    solver.set("produce-unsat-cores", "true")
    solver.set("minimal-unsat-cores", "true")

    solver.add(formulas)
    rsat = solver.check()

    return (rsat, solver)
    

