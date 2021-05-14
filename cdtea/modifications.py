from cdtea.simplicial import Triangulation, SimplexKey, DimDSimplexKey, Dim0SimplexKey, simplex_key
from cdtea.generate_flat import generate_flat_2d_space_time as gen
from cdtea.tests import valid_triangulation as validity
from cdtea.util.TimeIndex import time_sep
from functools import reduce

tri = gen(space_size=5, time_size=5)


def parity_move(triangulation: Triangulation, k1: SimplexKey, k2: SimplexKey):
    """
    |/| -> |\|
    """
    overlap = k1 & k2
    union = k1 | k2
    non_overlap = union - overlap
    # print(union)
    if overlap in triangulation.simplices[1]:
        s_type = triangulation.simplex_meta[overlap]["s_type"]
        if s_type == (1, 1):
            meta = triangulation.simplex_meta
            # This is where we modify the triangulation
            # The dim 0 simplices remain unchanged.

            for b in overlap:
                meta[b]["order"] -= 1
            for b in non_overlap:
                meta[b]["order"] += 1

            # the dim 1 simplices. the spatial edge is removed and replaced with another
            triangulation.remove_simplex(overlap)
            triangulation.add_simplex(non_overlap, s_type=(1, 1))

            # the dim 2 simplices, the two associated with the overlap are removed and the two new ones added
            triangulation.remove_simplex(k1)
            triangulation.remove_simplex(k2)

            overlap_list = overlap.basis_list
            times = [meta[b]['t'] for b in overlap_list]
            times = {b: time_sep(min(times), meta[b]['t'], triangulation.time_size) for b in overlap_list}
            overlap_list = sorted(overlap_list, key=lambda x: times[x])

            triangulation.add_simplex(non_overlap | overlap_list[0], s_type=(2, 1))
            triangulation.add_simplex(non_overlap | overlap_list[1], s_type=(1, 2))

            pass
        else:
            raise Exception("Faces are temporal neighbors not spatial neighbors")
    else:
        raise Exception("Faces are not neighbors")


def increase_move(triangulation: Triangulation, k1: SimplexKey, k2: SimplexKey):
    """
        /__\  ->  /|\
        \ /       \|/
    """
    overlap = k1 & k2
    union = k1 | k2
    non_overlap = union - overlap
    # print(union)
    if overlap in triangulation.simplices[1]:
        s_type = triangulation.simplex_meta[overlap]["s_type"]
        if s_type == (2, 0):
            meta = triangulation.simplex_meta
            # This is where we modify the triangulation
            # The dim 0 simplices remain unchanged.
            top = k1 - overlap
            bottom = k2 - overlap
            overlap_list = overlap.basis_list
            left = overlap_list[0]
            right = overlap_list[1]

            new_node = simplex_key(triangulation.max_index)

            triangulation.add_simplex(new_node, t=meta[right]['t'], order=4)
            meta[top]["order"] += 1
            meta[bottom]["order"] += 1

            # the dim 1 simplices. the spatial edge is removed and replaced with another
            triangulation.remove_simplex(overlap)

            triangulation.add_simplex(top | new_node, s_type=(1, 1))
            triangulation.add_simplex(bottom | new_node, s_type=(1, 1))

            triangulation.add_simplex(left | new_node, s_type=(2, 0))
            triangulation.add_simplex(right | new_node, s_type=(2, 0))

            # the dim 2 simplices, the two associated with the overlap are removed and the two new ones added
            k1_s_type = meta[k1]["s_type"]
            k2_s_type = meta[k2]["s_type"]

            triangulation.add_simplex(top | new_node | left, s_type=k1_s_type)
            triangulation.add_simplex(top | new_node | right, s_type=k1_s_type)

            triangulation.add_simplex(bottom | new_node | left, s_type=k2_s_type)
            triangulation.add_simplex(bottom | new_node | right, s_type=k2_s_type)

            triangulation.remove_simplex(k1)
            triangulation.remove_simplex(k2)


        else:
            raise Exception("Faces are spatial neighbors not temporal neighbors")
    else:
        raise Exception("Faces are not neighbors")


def decrease_move(triangulation: Triangulation, k1: SimplexKey):
    """
             /|\   ->  /__\
             \|/       \ /
    """
    meta = triangulation.simplex_meta

    if meta[k1]["order"] == 4:
        t_index = meta[k1]["t"]
        faces = [f for f in triangulation.simplices[2] if k1 in f]
        union = reduce(lambda x, y: x | y, faces) - k1
        space_neighbors = [b for b in union if meta[b]["t"] == t_index]
        spatial_edge = space_neighbors[0] | space_neighbors[1]

        triangulation.add_simplex(spatial_edge, s_type=(2, 0))



        for b in union - spatial_edge:
            meta[b]["order"] -= 1
        triangulation.remove_simplex(k1)
        for f in faces:
            # THIS DOUBLE ADDS SIMPLEX but because its a set it shouldn't be double counted.
            triangulation.add_simplex((f - k1) | spatial_edge, s_type=meta[f]["s_type"])
            triangulation.remove_simplex(f)

        for v in union:
            triangulation.remove_simplex(v | k1)
        pass
    else:
        raise Exception("vertex {} is not of order 4".format(k1))


key1 = simplex_key({1, 21, 22})
key2 = simplex_key({1, 2, 22})
key1 = simplex_key({10, 6, 5})
key2 = simplex_key({1, 6, 5})
increase_move(tri, key1, key2)
validity.is_valid(tri)
decrease_move(tri, simplex_key(25))
validity.is_valid(tri)
