# vertex/edge/triangle count
from cdtea import simplicial
from collections import defaultdict
from itertools import combinations, permutations


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


def edges_imply_faces(triangulation: simplicial.Triangulation) -> bool:
    edges = {e._basis for e in triangulation._simplices[1]}
    tris = {t._basis for t in triangulation._simplices[2]}
    sets_of_3_edges = combinations(edges, 3)
    faces = set()
    for edge_set in sets_of_3_edges:
        possible_face = frozenset.union(*edge_set)
        if len(possible_face) == 3:
            faces.add(possible_face)
    if tris == faces:
        return True
    elif tris.issubset(faces):
        print("This test is inconclusive. It's possible that there is a space-like or time-like loop of only length three")


def faces_imply_edges(triangulation: simplicial.Triangulation) -> bool:
    connections = set()
    edges = {e._basis for e in triangulation._simplices[1]}
    faces = {t._basis for t in triangulation._simplices[2]}
    for f in faces:
        edges_implied = combinations(f, 2)
        edges_implied = {frozenset(e) for e in edges_implied}
        connections = connections.union(edges_implied)
    return connections == edges




def is_valid(triangulation: simplicial.Triangulation) -> bool:
    res = True
    res = res and d_simplex_connects_2_dp1_simplices(triangulation)
    # res = res and twice_as_many_2d_as_0d(triangulation)
    return res
