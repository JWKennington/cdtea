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

    # Remove # TODO simplify this step to not require two loops
    to_remove = {edge, }
    for k in range(edge.dim + 1, 2 + 1):  # TODO add a 'dim' attribute to Triangulation
        to_remove = to_remove.union(trg.contains(edge, dim=k))

    for r in to_remove:
        trg.remove_simplex(r)

    # Add
    new_simplices = []
    new_simplices.append((simplicial.Dim0SimplexKey(trg.max_index + 1), {'t': orig_layer}))  # TODO test the new number
    new_simplices = ([(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (2, 0)}) for old in orig_nodes] +
                     [(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (1, 1)}) for old in nodes.difference(orig_nodes)])

    new_simplices.extend([(simplicial.DimDSimplexKey({new_vertex, old, fut_orig}), {'s_type': (2, 1)}) for old in orig_nodes])
    new_simplices.extend([(simplicial.DimDSimplexKey({new_vertex, old, past_orig}), {'s_type': (1, 2)}) for old in orig_nodes])

    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)

    trg.simplex_meta['order'][new_vertex] = 4
    trg.simplex_meta['order'][fut_orig] += 1
    trg.simplex_meta['order'][past_orig] += 1