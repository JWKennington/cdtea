"""
A set of utility functions for extracting information about triangulations
"""
from __future__ import annotations

from typing import Tuple

import numpy as np

from cdtea.simplicial import Dim0SimplexKey, Triangulation


def time_order(node1: Dim0SimplexKey, node2: Dim0SimplexKey, trg: Triangulation) -> Tuple[Dim0SimplexKey, Dim0SimplexKey]:
    t1, t2 = trg.simplex_meta['t'][node1], trg.simplex_meta['t'][node2]
    dt = time_sep(t1, t2, time_max=trg.time_size)
    if dt < 0:
        return (node2, node1)
    return (node1, node2)


def time_sep(t1: int, t2: int, time_max: int):
    """ Calculate the separation amount and direction of two time slices"""
    if not (isinstance(t1, int) and isinstance(t1, int)):
        raise TypeError(f"t1={t1} and t2={t2} must be ints")

    i = (t1 - t2)
    j = (t2 - t1)

    if time_max is not None:
        i = i % time_max
        j = j % time_max

    if j > i:
        return -i
    return j


def nearest(ref, pnt):
    deltas = np.array([[0, 1], [1, 0], [1, 1], [0, -1], [-1, 0], [-1, -1]]) * 2 * np.pi
    sep = np.linalg.norm(pnt - ref)
    final_delta = np.array([0, 0])
    for delta in deltas:
        test_sep = np.linalg.norm(pnt + delta - ref)
        if test_sep < sep:
            sep = test_sep
            final_delta = delta
    return pnt + final_delta


def get_layer(st: Triangulation, t: int):
    if 0 <= t < st.time_size and isinstance(t, int):
        return list(st.simplex_meta['t'].dual[t])
    raise ValueError(f"t={t} must be between 0 and {st.time_size} and be an int")


def spatial_ordering(st: Triangulation, layer: list[Dim0SimplexKey], indexed: list[Dim0SimplexKey] = None):
    """
    returns an ordered array of nodes

    note that there are two valid orderings 01234 or 43210

    layer: a list containing all the verts with the same time index

    indexed: if a first and second vertex are supplied then there is only a single valid ordering

    an ordering is produced by starting at a particular vertex and finding the subsequent spatially adjacent vertex
    until all vertices are indexed.
    """

    # if origin is unspecified chose a random origin
    if indexed is None:
        indexed = [layer[0]]
        origin = indexed[0]
        # the current "edge" of the ordering
        boundary = origin
    else:
        boundary = indexed[1]

    # all nodes that are not yet indexed
    not_indexed = set(layer) - set(indexed)

    # each iteration adds one new node to the index dict. therefore we need to loop once for each item in layer
    for _ in range(len(layer)):

        # for each link in the chain we want to find an item which is connected to the boundary and not yet indexed
        for f in not_indexed:
            if f | boundary in st.edges:
                # remove f from not_indexed
                not_indexed -= {f}
                indexed.append(f)
                boundary = f

                # once one has been found we can move on to the next loop
                break
    return indexed


def get_shared_future(v1, v2, st: Triangulation):
    triangles_containg_v1 = st.contains(v1, dim=2)
    triangles_containg_v2 = st.contains(v2, dim=2)
    vt_0, vt_1 = st.flatten(triangles_containg_v1 & triangles_containg_v2) - {v1, v2}
    dt = time_sep(st.simplex_meta['t'][v1], st.simplex_meta['t'][vt_0], st.time_size)
    if dt > 0:
        return vt_0
    if dt < 0:
        return vt_1


def get_layer_parity(past_layer, past_left_vert, past_right_vert, st):
    """ Given the orientation of the previous layer gives an orientation for layer that is aligned.

    New Plan:
    - find common future point of past left and past right (done)
    - find spacelike edges of common future point (done)
    - find two additional vertices of the spacelike edges (for a total of three vertices) (done)
    - check if new vertex in future(past_right), then (common, new) is the right order, else (new, common)
    
    """
    # left, right = None, None
    middle = get_shared_future(past_left_vert, past_right_vert, st)
    space_like_edges_of_middle = [e for e in st.contains(middle, dim=1) if st.simplex_meta['s_type'][e] == (2, 0)]
    new_verts = st.flatten(space_like_edges_of_middle) - {middle, }
    past_leftmost, past_rightmost = past_left_vert, past_right_vert
    past_leftmost_index, past_rightmost_index = past_layer.index(past_leftmost), past_layer.index(past_rightmost)

    #TODO this fails when time size is less than 5? wtf?
    #This gets stuck in an infinite loop, past layer seems to only include two verts
    while past_leftmost in st.flatten(st.contains(middle, dim=1)):
        past_leftmost_index = (past_leftmost_index - 1) % len(past_layer)
        past_leftmost = past_layer[past_leftmost_index]
    past_leftmost = past_layer[(past_leftmost_index + 1) % len(past_layer)]
    while past_rightmost in st.flatten(st.contains(middle, dim=1)):
        past_rightmost_index = (past_rightmost_index + 1) % len(past_layer)
        past_rightmost = past_layer[past_rightmost_index]
    past_rightmost = past_layer[(past_rightmost_index - 1) % len(past_layer)]

    for vert in new_verts:
        if vert in st.flatten(st.contains(past_leftmost, dim=1)):
            left = vert
        if vert in st.flatten(st.contains(past_rightmost, dim=1)):
            right = vert
    return left, middle, right


def total_ordering(st: Triangulation):
    """ Produces a list of each layer ordered and with the same parity."""
    layers = {t: get_layer(st, t) for t in range(st.time_size)}

    base_order = spatial_ordering(st, layers[0])

    prev_orientation = base_order[0:2]
    total_order = [base_order]
    for t in range(1, st.time_size):
        past_left_vert, past_right_vert = prev_orientation[0:2]
        left, middle, right = get_layer_parity(total_order[t - 1], past_left_vert, past_right_vert, st)

        if t % 2 == 0:
            order = spatial_ordering(st, layers[t], indexed=[middle, right])
        else:
            order = spatial_ordering(st, layers[t], indexed=[left, middle])
        prev_orientation = order[0:2]
        total_order.append(order)
    return total_order
