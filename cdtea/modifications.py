"""
Tools to modify a triangulation while preserving its validity.
"""

import random
from functools import reduce

from cdtea.simplicial import Triangulation, SimplexKey, simplex_key
from cdtea.util.triangulation_utils import time_sep


def parity_move(triangulation: Triangulation, k1: SimplexKey, k2: SimplexKey):
    r"""
    |k1/k2| -> |\|

    k1 and k2 are simplex keys for triangles. They should be spatialy adjacent. This function swaps their connecting edge.
    """
    overlap = k1 & k2
    meta = triangulation.simplex_meta

    # Test that k1 and k2 are spatial neighbors.
    if overlap not in triangulation.edges:
        raise Exception("Faces are not neighbors")

    s_type = triangulation.simplex_meta["s_type"][overlap]
    if s_type != (1, 1):
        raise Exception("Faces are temporal neighbors not spatial neighbors")

    union = k1 | k2
    non_overlap = union - overlap

    # This is where we modify the triangulation
    # The dim 0 simplices remain unchanged.

    for b in overlap:
        meta["order"][b] -= 1
    for b in non_overlap:
        meta["order"][b] += 1

    # the dim 1 simplices. the spatial edge is removed and replaced with another
    triangulation.remove_simplex(overlap)
    triangulation.add_simplex(non_overlap, s_type=(1, 1))

    # the dim 2 simplices, the two associated with the overlap are removed and the two new ones added
    triangulation.remove_simplex(k1)
    triangulation.remove_simplex(k2)

    overlap_list = overlap.basis_list
    times = [meta['t'][b] for b in overlap_list]
    times = {b: time_sep(min(times), meta['t'][b], triangulation.time_size) for b in overlap_list}
    overlap_list = sorted(overlap_list, key=lambda x: times[x])

    triangulation.add_simplex(non_overlap | overlap_list[0], s_type=(2, 1), dilation=random.Random())
    triangulation.add_simplex(non_overlap | overlap_list[1], s_type=(1, 2), dilation=random.Random())


def increase_move(triangulation: Triangulation, k1: SimplexKey, k2: SimplexKey):
    r"""
        /__\  ->  /|\
        \ /       \|/
    """
    overlap = k1 & k2
    if overlap in triangulation.edges:
        s_type = triangulation.simplex_meta["s_type"][overlap]
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

            triangulation.add_simplex(new_node, t=meta['t'][right], order=4)
            meta["order"][top] += 1
            meta["order"][bottom] += 1

            # the dim 1 simplices. the spatial edge is removed and replaced with another
            triangulation.remove_simplex(overlap)

            triangulation.add_simplex(top | new_node, s_type=(1, 1))
            triangulation.add_simplex(bottom | new_node, s_type=(1, 1))

            triangulation.add_simplex(left | new_node, s_type=(2, 0))
            triangulation.add_simplex(right | new_node, s_type=(2, 0))

            # the dim 2 simplices, the two associated with the overlap are removed and the two new ones added
            k1_s_type = meta["s_type"][k1]
            k2_s_type = meta["s_type"][k2]

            triangulation.add_simplex(top | new_node | left, s_type=k1_s_type, dilation=random.Random())
            triangulation.add_simplex(top | new_node | right, s_type=k1_s_type, dilation=random.Random())

            triangulation.add_simplex(bottom | new_node | left, s_type=k2_s_type, dilation=random.Random())
            triangulation.add_simplex(bottom | new_node | right, s_type=k2_s_type, dilation=random.Random())

            triangulation.remove_simplex(k1)
            triangulation.remove_simplex(k2)

        else:
            raise Exception("Faces are spatial neighbors not temporal neighbors")
    else:
        raise Exception("Faces are not neighbors")


def decrease_move(triangulation: Triangulation, k1: SimplexKey):
    r"""
             /|\   ->  /__\
             \|/       \ /
    """
    meta = triangulation.simplex_meta

    if meta["order"][k1] != 4:
        raise Exception(f"vertex {k1} is not of order 4")
    t_index = meta["t"][k1]
    faces = [f for f in triangulation.simplices[2] if k1 in f]
    union = reduce(lambda x, y: x | y, faces) - k1
    space_neighbors = [b for b in union if meta["t"][b] == t_index]
    spatial_edge = space_neighbors[0] | space_neighbors[1]

    triangulation.add_simplex(spatial_edge, s_type=(2, 0))

    for b in union - spatial_edge:
        meta["order"][b] -= 1
    triangulation.remove_simplex(k1)
    for f in faces:
        # THIS DOUBLE ADDS SIMPLEX but because its a set it shouldn't be double counted.
        triangulation.add_simplex((f - k1) | spatial_edge, s_type=meta["s_type"][f], dilation=random.Random())
        triangulation.remove_simplex(f)

    for v in union:
        triangulation.remove_simplex(v | k1)
