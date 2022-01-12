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

    # Remove # TODO simplify this step to not require two loops
    to_remove = {edge, }
    for k in range(edge.dim + 1, 2 + 1):  # TODO add a 'dim' attribute to Triangulation
        to_remove = to_remove.union(trg.contains(edge, dim=k))

    for r in to_remove:
        trg.remove_simplex(r)

    # Add
    new_vertex = simplicial.Dim0SimplexKey(trg.max_index + 1)  # TODO test the new number
    new_edges = ([(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (2, 0)}) for old in orig_nodes] +
                 [(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (1, 1)}) for old in nodes.difference(orig_nodes)])
    
    new_triangles = []
    for old1 in orig_nodes:
        for old2 in nodes.difference(orig_nodes):
            if time_sep(orig_layer, trg.simplex_meta['t'][old2], trg.time_size) > 0:
                type = (2, 1)
            elif time_sep(orig_layer, trg.simplex_meta['t'][old2], trg.time_size) < 0:
                type = (1, 2)
            new_triangles.append((simplicial.DimDSimplexKey({new_vertex, old1, old2}), {'s_type': type}))

    trg.add_simplex(new_vertex, t=orig_layer)
    trg.simplex_meta['order'][new_vertex] = 4
    for new, kwargs in new_edges:
        trg.add_simplex(new, **kwargs)

    for n in nodes.difference(orig_nodes):
        trg.simplex_meta['order'][n] += 1

    for new, kwargs in new_triangles:
        trg.add_simplex(new, **kwargs)
