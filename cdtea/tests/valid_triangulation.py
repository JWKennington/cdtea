""" Various tests that a triangulation must past to be a valid toroidal 1+1d simplicial manifold."""
from itertools import combinations
from collections import defaultdict

from cdtea import simplicial
from cdtea.util.triangulation_utils import time_sep


# These tests assume 1+1d with toroidal topology

def twice_as_many_2d_as_0d(triangulation: simplicial.Triangulation):
    """For toroidal topology in 1+1d there should be twice as many faces as vertices"""
    number_of_vertices = len(triangulation.simplices[0])
    number_of_faces = len(triangulation.simplices[2])
    err_msg = "The number of triangles was not twice the number of vertices"
    assert 2 * number_of_vertices == number_of_faces, err_msg


def edges_imply_faces(triangulation: simplicial.Triangulation):
    """ Attempts to generate the set of faces from the set of edges"""
    edges = triangulation.simplices[1]
    tris = triangulation.simplices[2]
    sets_of_3_edges = combinations(edges, 3)
    faces = set()
    for edge_set in sets_of_3_edges:
        possible_face = edge_set[0] | edge_set[1] | edge_set[2]
        if possible_face.dim == 2:
            faces.add(possible_face)
    # They should be equal if there are no slices of length 3
    assert tris.issubset(faces), "The implied faces did not contain all the given faces"


def faces_imply_edges(triangulation: simplicial.Triangulation):
    """ Attempts to generate the set of edges from the set of faces"""
    connections = set()
    edges = triangulation.simplices[1]
    faces = triangulation.simplices[2]
    for f in faces:
        edges_implied = {simplicial.simplex_key(b) for b in combinations(f, 2)}
        connections = connections.union(edges_implied)
    assert connections == edges, "the set of edges implied by faces is not the same as the given edges"


# It may be redundant to have both of the following two and the previous 2
def edges_imply_nodes(triangulation: simplicial.Triangulation):
    """ Generate the set of all nodes used in edges"""
    verts = set()
    nodes = triangulation.simplices[0]
    for e in triangulation.simplices[1]:
        # union equals
        verts |= e.basis
    assert verts == nodes, "the set of vertices used in edges is not the same as the given vertices"


def faces_imply_nodes(triangulation: simplicial.Triangulation):
    """generate the set of nodes used in faces"""
    verts = set()
    nodes = triangulation.simplices[0]
    tris = triangulation.simplices[2]
    for f in tris:
        # union equals
        verts |= f.basis
    assert verts == nodes, "the set of vertices used in faces is not the same as the given vertices"


def edges_dont_cross_time_slices(triangulation: simplicial.Triangulation):
    """check that all edges connect either the same time slice or adjacent time slices"""
    edges = triangulation.simplices[1]
    for e in edges:
        constituent_verts = e.basis_list
        n0 = constituent_verts[0]
        n1 = constituent_verts[1]
        t0 = triangulation.simplex_meta["t"][n0]
        t1 = triangulation.simplex_meta["t"][n1]
        dt = abs(t1 - t0) % (triangulation.time_size - 2)
        assert dt <= 1, f"The time separation between {n0} and {n1} is {dt}"


def vertices_have_minimum_required_connections(triangulation: simplicial.Triangulation):
    """check that every vertex has 2 spatial edges"""
    edges = triangulation.simplices[1]
    verts = triangulation.simplices[0]
    time_size = triangulation.time_size

    counts_spatial, counts_past, counts_future = defaultdict(int), defaultdict(int), defaultdict(int)

    for e in edges:
        s_type = triangulation.simplex_meta["s_type"][e]
        basis = e.basis_list

        # if it is a spatial edge add one to the spatial connection for both constituent vertices
        if s_type == (2, 0):
            for v in basis:
                counts_spatial[v] += 1

        # if it is a temporal edge figure out past and future and augment the appropriate lists
        elif s_type == (1, 1):
            t0 = triangulation.simplex_meta["t"][basis[0]] % time_size
            t1 = triangulation.simplex_meta["t"][basis[1]] % time_size
            t0_offset = (t0 + time_size / 2) % time_size
            t1_offset = (t1 + time_size / 2) % time_size
            if t1 - t0 == 1 or t1_offset - t0_offset == 1:
                counts_future[basis[0]] += 1
                counts_past[basis[1]] += 1
            elif t0 - t1 == 1 or t0_offset - t1_offset == 1:
                counts_future[basis[1]] += 1
                counts_past[basis[0]] += 1
            else:
                raise Exception("s_type {type} does not match, both basis have the same time ".format(type=s_type))
        else:
            raise Exception("invalid s_type {type}".format(type=s_type))

    counts_spatial, counts_future, counts_past = dict(counts_spatial), dict(counts_future), dict(counts_past)

    for v in verts:
        assert counts_spatial[v] == 2, f"{v} has {counts_spatial[v]} spatial neighbors"
        assert counts_future[v] > 0, f"{v} has {counts_spatial[v]} future connections"
        assert counts_past[v] > 0, f"{v} has {counts_spatial[v]} past connections"


def check_s_type(triangulation: simplicial.Triangulation):
    """Cheks the s_type of all edges and triangles"""
    meta = triangulation.simplex_meta

    time_index = meta['t']

    # Checks the edges
    for e in triangulation.simplices[1]:
        basis_list = e.basis_list
        dt = time_sep(time_index[basis_list[0]], time_index[basis_list[1]], triangulation.time_size)
        if dt == 0:
            assert meta['s_type'][e] == (2, 0)
        elif abs(dt) == 1:
            assert meta['s_type'][e] == (1, 1)
        else:
            raise Exception("invalid edge")
    # checks the triangles
    for f in triangulation.simplices[2]:

        times = [time_index[b] for b in f]
        times = [time_sep(min(times), time_index[b], triangulation.time_size) for b in f]
        c1 = times.count(min(times))
        if c1 == 2:
            assert meta["s_type"][f] == (2, 1)
        elif c1 == 1:
            assert meta["s_type"][f] == (1, 2)

# Check if Dim0Simpplex order is correct
def test_order(triangulation: simplicial.Triangulation):
    """Cheks the s_type of all edges and triangles"""
    meta = triangulation.simplex_meta

    for n in triangulation.nodes:
        assert meta['order'][n] == len([e for e in triangulation.edges if n in e])


def is_valid(triangulation: simplicial.Triangulation):
    twice_as_many_2d_as_0d(triangulation)
    edges_imply_faces(triangulation)
    faces_imply_edges(triangulation)
    edges_imply_nodes(triangulation)
    faces_imply_nodes(triangulation)
    edges_dont_cross_time_slices(triangulation)
    vertices_have_minimum_required_connections(triangulation)
    check_s_type(triangulation)
    test_order(triangulation)
