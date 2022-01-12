"""Moves

"""
import numpy as np
from scipy.stats import mode

from cdtea import simplicial
from cdtea.util.triangulation_utils import time_sep


def add_2D(trg: simplicial.Triangulation, edge: simplicial.SimplexKey):
    """

    Args:
        trg:
        edge:

    Returns:

    """
    # Discovery
    faces = trg.contains(edge, dim=2)
    nodes = trg.flatten(faces)
    orig_nodes = trg.contains(edge, dim=0)
    orig_layer = trg.simplex_meta['t'][list(orig_nodes)[0]]
    fut_orig, past_orig = nodes.difference(orig_nodes)
    if trg.simplex_meta['t'][past_orig] > trg.simplex_meta['t'][fut_orig]:
        fut_orig, past_orig = past_orig, fut_orig

    # TODO implement utility for time ordering nodes
    fut_t, node_t, past_t = trg.simplex_meta['t'][fut_orig], trg.simplex_meta['t'][list(orig_nodes)[0]], trg.simplex_meta['t'][past_orig]

    if abs(fut_t - node_t) == 1 and abs(node_t - past_t) == 1:  # Fully adjacent, no boundary overlap
        if trg.simplex_meta['t'][past_orig] > trg.simplex_meta['t'][fut_orig]:
            fut_orig, past_orig = past_orig, fut_orig
    else:  # one node crosses boundary
        if fut_t - node_t == -1 or node_t - past_t == -1:  # Not the correct ordering
            fut_orig, past_orig = past_orig, fut_orig

    # Remove # TODO simplify this step to not require two loops
    to_remove = {edge, }
    for k in range(edge.dim + 1, 2 + 1):  # TODO add a 'dim' attribute to Triangulation
        to_remove = to_remove.union(trg.contains(edge, dim=k))

    for r in to_remove:
        trg.remove_simplex(r)

    # Add
    new_vertex = simplicial.Dim0SimplexKey(trg.max_index + 1)
    new_simplices = []
    new_simplices.append((new_vertex, {'t': orig_layer}))  # TODO test the new number
    new_simplices.extend(([(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (2, 0)}) for old in orig_nodes] +
                          [(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (1, 1)}) for old in nodes.difference(orig_nodes)]))

    new_simplices.extend([(simplicial.DimDSimplexKey({new_vertex, old, fut_orig}), {'s_type': (2, 1)}) for old in orig_nodes])
    new_simplices.extend([(simplicial.DimDSimplexKey({new_vertex, old, past_orig}), {'s_type': (1, 2)}) for old in orig_nodes])

    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)

    # Meta
    trg.simplex_meta['order'][new_vertex] = 4
    trg.simplex_meta['order'][fut_orig] += 1
    trg.simplex_meta['order'][past_orig] += 1


def rem_2D(trg: simplicial.Triangulation, node: simplicial.DimDSimplexKey):
    """

    Args:
        trg:
        edge:

    Returns:

    """
    # Discovery
    edges = trg.contains(node, dim=1)
    spacelike_edges = [e for e in edges if trg.simplex_meta['s_type'][e] == (2, 0)]
    timelike_edges = [e for e in edges if trg.simplex_meta['s_type'][e] == (1, 1)]
    spacelike_neighbors = trg.contains(spacelike_edges[0], dim=0).union(trg.contains(spacelike_edges[1], dim=0)).difference({node})


    fut_orig, past_orig = trg.contains(timelike_edges[0], dim=0).union(trg.contains(timelike_edges[1], dim=0)).difference({node})

    # TODO implement utility for time ordering nodes
    fut_t, node_t, past_t = trg.simplex_meta['t'][fut_orig], trg.simplex_meta['t'][node], trg.simplex_meta['t'][past_orig]

    if abs(fut_t - node_t) == 1 and abs(node_t - past_t) == 1: # Fully adjacent, no boundary overlap
        if trg.simplex_meta['t'][past_orig] > trg.simplex_meta['t'][fut_orig]:
            fut_orig, past_orig = past_orig, fut_orig
    else: # one node crosses boundary
        if fut_t - node_t == -1 or node_t - past_t == -1: # Not the correct ordering
            fut_orig, past_orig = past_orig, fut_orig

    # Remove # TODO simplify this step to not require two loops
    to_remove = {node}
    for edge in edges:
        to_remove = to_remove.union({edge})
        for k in range(edge.dim + 1, 2 + 1):  # TODO add a 'dim' attribute to Triangulation
            to_remove = to_remove.union(trg.contains(edge, dim=k))

    for r in to_remove:
        trg.remove_simplex(r)

    # Add
    new_simplices = [
        (simplicial.DimDSimplexKey(spacelike_neighbors), {'s_type': (2, 0)}),
        (simplicial.DimDSimplexKey(spacelike_neighbors.union({fut_orig})), {'s_type': (2, 1)}),
        (simplicial.DimDSimplexKey(spacelike_neighbors.union({past_orig})), {'s_type': (1, 2)}),
    ]

    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)

    # Meta
    trg.simplex_meta['order'][fut_orig] -= 1
    trg.simplex_meta['order'][past_orig] -= 1
