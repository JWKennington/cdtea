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
    """For toroidal topology in 1+1d there should be twice as many faces as vertices"""
    assert len(triangulation._simplices[0]) * 2 == len(triangulation._simplices[2]), "The number of triangles was not twice the number of vertices"


def edges_imply_faces(triangulation: simplicial.Triangulation) -> bool:
    edges = {e._basis for e in triangulation._simplices[1]}
    tris = {t._basis for t in triangulation._simplices[2]}
    sets_of_3_edges = combinations(edges, 3)
    faces = set()
    for edge_set in sets_of_3_edges:
        possible_face = frozenset.union(*edge_set)
        if len(possible_face) == 3:
            faces.add(possible_face)
    #They should be equal if there are no slices of length 3 
    assert tris.issubset(faces), "The implied faces did not contain all the given faces"


def faces_imply_edges(triangulation: simplicial.Triangulation) -> bool:
    connections = set()
    edges = {e._basis for e in triangulation._simplices[1]}
    faces = {t._basis for t in triangulation._simplices[2]}
    for f in faces:
        edges_implied = combinations(f, 2)
        edges_implied = {frozenset(e) for e in edges_implied}
        connections = connections.union(edges_implied)
    assert connections == edges, "the set of edges implied by faces is not the same as the given edges"
    

def edges_imply_nodes(triangulation: simplicial.Triangulation) -> bool:
    verts = set()
    edges = {e._basis for e in triangulation._simplices[1]}
    nodes = {n._basis for n in triangulation._simplices[0]}
    for e in edges:
        verts_implied = {frozenset([b]) for b in e}
        verts = verts.union(verts_implied)
    assert verts == nodes, "the set of vertices used in edges is not the same as the given vertices"

def faces_imply_nodes(triangulation: simplicial.Triangulation) -> bool:
    verts = set()
    faces = {f._basis for f in triangulation._simplices[2]}
    nodes = {n._basis for n in triangulation._simplices[0]}
    for f in faces:
        verts_implied = {frozenset([b]) for b in f}
        verts = verts.union(verts_implied)
    assert verts == nodes, "the set of vertices used in faces is not the same as the given vertices"





def is_valid(triangulation: simplicial.Triangulation) -> bool:
    twice_as_many_2d_as_0d(triangulation)
    edges_imply_faces(triangulation)
    faces_imply_edges(triangulation)
    edges_imply_nodes(triangulation)
    faces_imply_nodes(triangulation)
    
