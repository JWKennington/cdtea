"""Moves

"""
import numpy as np
from scipy.stats import mode

from cdtea import simplicial


def add_2D(trg: simplicial.Triangulation, edge: simplicial.SimplexKey):
    """

    Args:
        trg:
        edge:

    Returns:

    """
    # Discovery
    print(edge)
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
    new_simplices = ([(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (2, 0)}) for old in orig_nodes] +
                     [(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (1, 1)}) for old in nodes.difference(orig_nodes)])
    for old1 in orig_nodes:
        for old2 in nodes.difference(orig_nodes):
            if orig_layer < trg.simplex_meta['t'][old2]:
                type = (2, 1)
            elif orig_layer > trg.simplex_meta['t'][old2]:
                type = (1, 2)
            new_simplices.append((simplicial.DimDSimplexKey({new_vertex, old1, old2}), {'s_type': type}))

    trg.add_simplex(new_vertex, t=orig_layer)
    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)
