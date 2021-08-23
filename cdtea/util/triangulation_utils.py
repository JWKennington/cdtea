from __future__ import annotations
import numpy as np
from cdtea.simplicial import Dim0SimplexKey, Triangulation


def time_sep(t1: int, t2: int, time_max: int):
    """ Calculate the separation amount and direction of two time slices"""
    i = (t1 - t2) % time_max
    j = (t2 - t1) % time_max
    if i < j:
        return -i
    if j <= i:
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
    if 0 <= t < st.time_size:
        return [n for n in st.nodes if st.simplex_meta[n]['t'] == t]
    raise ValueError(f"t={t} must be between 0 and {st.time_size}")


def spatial_ordering(st: Triangulation, layer: list[Dim0SimplexKey], indexed: list[Dim0SimplexKey] = None):
    """
    returns an ordered array of nodes

    note that there are two valid orderings 01234 or 43210

    layer: a list constaining all the verts with the same time index

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
    for i in range(len(layer)):

        # for each link in the chain we want to find an item which is connected to the boundary and not yet indexed
        for f in not_indexed:
            if (f | boundary) in st.simplices[1]:
                # remove f from not_indexed
                not_indexed -= {f}
                indexed.append(f)
                boundary = f

                # once one has been found we can move on to the next loop
                break
    return indexed


def total_ordering(st: Triangulation):
    layers = {t: get_layer(st, t) for t in range(st.time_size)}

    base_order = spatial_ordering(st, layers[0])

    prev_orientation = base_order[0:2]
    total_order = [base_order]
    for t in range(1, st.time_size):
        layer = layers[t]
        past_left_vert, past_right_vert = prev_orientation[0:2]
        for vert in layer:

            left_overlap, right_overlap = vert | past_left_vert, vert | past_right_vert
            connected_left, connected_right = left_overlap in st.edges, right_overlap in st.edges

            if connected_left and connected_right:
                middle = vert
            elif connected_right:
                right = vert
            elif connected_left:
                left = vert

        if t % 2 == 0:
            ORD = spatial_ordering(st, layers[t], indexed=[middle, right])
        else:
            ORD = spatial_ordering(st, layers[t], indexed=[left, middle])
        prev_orientation = ORD[0:2]
        total_order.append(ORD)
    return total_order
