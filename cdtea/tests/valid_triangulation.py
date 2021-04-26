# vertex/edge/triangle count
from cdtea import simplicial
from collections import defaultdict
from itertools import combinations


# 2d only


def d_simplex_connects_2_dp1_simplices(triangulation: simplicial.Triangulation) -> bool:
    """This function checks that each d simplex has two and only two d+1 super simplices."""
    counts = defaultdict(int)
    # d is one minus the dim of the triangulation
    d = 2 - 1
    for tri in triangulation._simplices[d + 1]:
        combs = combinations(tri.basis_list, d + 1)
        for edge_basis in combs:

            counts[frozenset(edge_basis)] += 1
    counts = dict(counts)
    res = True
    for edge in triangulation._simplices[d]:
        b = frozenset(edge.basis_list)
        res = res and (counts[b] == 2)
    return res


def twice_as_many_2d_as_0d(triangulation: simplicial.Triangulation) -> bool:
    """This function checks that each d simplex has two and only two d+1 super simplices."""
    return (triangulation._simplices[0] * 2 == triangulation._simplices[2])


def is_valid(triangulation: simplicial.Triangulation) -> bool:
    res = True
    res = res and d_simplex_connects_2_dp1_simplices(triangulation)
    # res = res and twice_as_many_2d_as_0d(triangulation)
    return res