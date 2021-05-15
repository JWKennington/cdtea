from cdtea.generate_flat import generate_flat_2d_space_time
from matplotlib import pyplot as plt
from cdtea import simplicial
from cdtea.simplicial import simplex_key

tri = generate_flat_2d_space_time(space_size=10, time_size=10)
meta = tri.simplex_meta
slab_height = .1

origin = tri.simplices[0]


def x_path(tri: simplicial.Triangulation, v1: simplicial.Dim0SimplexKey, v2: simplicial.Dim0SimplexKey, possible_edges,
           used_edges=set()

           ):
    meta = tri.simplex_meta

    t = meta[v1]['t']
    if t != meta[v2]['t']:
        raise Exception("Not on the same time slice")
    else:
        if v1 == v2:
            return used_edges
        edges = possible_edges

        v = v1
        for e in edges - used_edges:
            new_v = e - v1
            if new_v.dim == 0:
                # print(new_v)
                return x_path(tri, new_v, v2, used_edges={e} | used_edges, possible_edges=possible_edges)


possible_edges = {}  # get all spatial edges
for e in tri.simplices[1]:
    basis = e.basis_list
    if meta[e]["s_type"] == (2, 0):
        if meta[basis[0]]['t'] == t and meta[basis[1]]['t'] == t:
            possible_edges.add(e)




x_path(tri, simplex_key(1), simplex_key(5), possible_edges)
