# vertex/edge/triangle count
from cdtea import simplicial
from collections import defaultdict
from itertools import combinations, permutations


# These tests assume 1+1d with toroidal topology

def twice_as_many_2d_as_0d(triangulation: simplicial.Triangulation) -> bool:
    """For toroidal topology in 1+1d there should be twice as many faces as vertices"""
    assert len(triangulation.simplices[0]) * 2 == len(
        triangulation.simplices[2]), "The number of triangles was not twice the number of vertices"


def edges_imply_faces(triangulation: simplicial.Triangulation):
    """ Attempts to generate the set of faces from the set of edges"""
    edges = {e.basis for e in triangulation.simplices[1]}
    tris = {t.basis for t in triangulation.simplices[2]}
    sets_of_3_edges = combinations(edges, 3)
    faces = set()
    for edge_set in sets_of_3_edges:
        possible_face = frozenset.union(*edge_set)
        if len(possible_face) == 3:
            faces.add(possible_face)
    # They should be equal if there are no slices of length 3
    assert tris.issubset(faces), "The implied faces did not contain all the given faces"


def faces_imply_edges(triangulation: simplicial.Triangulation):
    """ Attempts to generate the set of edges from the set of faces"""
    connections = set()
    edges = {e.basis for e in triangulation.simplices[1]}
    faces = {t.basis for t in triangulation.simplices[2]}
    for f in faces:
        edges_implied = combinations(f, 2)
        edges_implied = {frozenset(e) for e in edges_implied}
        connections = connections.union(edges_implied)
    assert connections == edges, "the set of edges implied by faces is not the same as the given edges"


def edges_imply_nodes(triangulation: simplicial.Triangulation):
    """ Generate the set of all nodes used in edges"""
    verts = set()
    edges = {e.basis for e in triangulation.simplices[1]}
    nodes = {n.basis for n in triangulation.simplices[0]}
    for e in edges:
        verts_implied = {b.basis for b in e}
        verts = verts.union(verts_implied)
    assert verts == nodes, "the set of vertices used in edges is not the same as the given vertices"


def faces_imply_nodes(triangulation: simplicial.Triangulation):
    """generate the set of nodes used in faces"""
    verts = set()
    faces = {f.basis for f in triangulation.simplices[2]}
    nodes = {n.basis for n in triangulation.simplices[0]}
    for f in faces:
        verts_implied = {b.basis for b in f}
        verts = verts.union(verts_implied)
    assert verts == nodes, "the set of vertices used in faces is not the same as the given vertices"


def edges_dont_cross_time_slices(triangulation: simplicial.Triangulation):
    """check that all edges connect either the same time slice or adjacent time slices"""
    edges = triangulation.simplices[1]
    for e in edges:
        constituent_verts = e.basis_list
        n0 = constituent_verts[0]
        n1 = constituent_verts[1]
        t0 = triangulation.simplex_meta[n0]["t"]
        t1 = triangulation.simplex_meta[n1]["t"]
        max_time_index = triangulation.time_size - 1
        dt = abs(t1 - t0) % max_time_index
        assert dt <= 1, "The time separation between {n0} and {n1} is {dt}".format(n0=n0, n1=n1, dt=dt)


def is_valid(triangulation: simplicial.Triangulation):
    twice_as_many_2d_as_0d(triangulation)
    edges_imply_faces(triangulation)
    faces_imply_edges(triangulation)
    edges_imply_nodes(triangulation)
    faces_imply_nodes(triangulation)
    edges_dont_cross_time_slices(triangulation)
