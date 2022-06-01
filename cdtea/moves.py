"""Moves

"""

from cdtea import simplicial
from cdtea.util import triangulation_utils
import random


def add_2d(trg: simplicial.Triangulation, edge: simplicial.SimplexKey):
    """

    Args:
        trg: The triangulation on which to make the move
        edge: a spatial edge that is a member of trg

     /\       -->      /|\
    /__\      -->     /_|_\
    \  /      -->     \ | /
     \/       -->      \|/

    modifies trg in place by performing a (2,4) type move which modifies a subcomplex of two temporaly adjacent triangles in to a subcomplex of 4 triangles.

    This move is described in detail in section 6.3 of "non-perturbative quantum gravity"

    """
    # Discovery
    faces = trg.contains(edge, dim=2)
    nodes = trg.flatten(faces)
    orig_nodes = trg.contains(edge, dim=0)
    orig_layer = trg.simplex_meta['t'][list(orig_nodes)[0]]
    fut_orig, past_orig = nodes.difference(orig_nodes)
    past_orig, fut_orig = triangulation_utils.time_order(past_orig, fut_orig, trg)

    # Remove # TODO simplify this step to not require two loops
    to_remove = {edge, }
    for k in range(edge.dim + 1, 2 + 1):  # TODO add a 'dim' attribute to Triangulation
        to_remove = to_remove.union(trg.contains(edge, dim=k))

    for r in to_remove:
        trg.remove_simplex(r)

    # Add

    new_vertex = simplicial.Dim0SimplexKey(trg.max_index)
    new_simplices = []
    new_simplices.append((new_vertex, {'t': orig_layer}))  # TODO test the new number
    new_simplices.extend(([(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (2, 0)}) for old in orig_nodes] +
                          [(simplicial.DimDSimplexKey({new_vertex, old}), {'s_type': (1, 1)}) for old in nodes.difference(orig_nodes)]))

    new_simplices.extend([(simplicial.DimDSimplexKey({new_vertex, old, fut_orig}), {'s_type': (2, 1), 'dilaton': random.random()}) for old in orig_nodes])
    new_simplices.extend([(simplicial.DimDSimplexKey({new_vertex, old, past_orig}), {'s_type': (1, 2), 'dilaton': random.random()}) for old in orig_nodes])

    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)

    # Meta
    trg.simplex_meta['order'][new_vertex] = 4
    trg.simplex_meta['order'][fut_orig] += 1
    trg.simplex_meta['order'][past_orig] += 1


def rem_2d(trg: simplicial.Triangulation, node: simplicial.DimDSimplexKey):
    """

    Args:
        trg: The triangulation on which to make the move
        node: a node of order 4 in the triangulation

       /|\   -->    /\
      /_|_\  -->   /__\
      \ | /  -->   \  /
       \|/   -->    \/

    modifies trg in place by performing a (4,2) type move which modifies a subcomplex of 4 adjacent triangles in to a subcomplex of 2 triangles.

    This move is described in detail in section 6.3 of "non-perturbative quantum gravity"

    """
    # Discovery
    edges = trg.contains(node, dim=1)
    spacelike_edges = [e for e in edges if trg.simplex_meta['s_type'][e] == (2, 0)]
    timelike_edges = [e for e in edges if trg.simplex_meta['s_type'][e] == (1, 1)]
    spacelike_neighbors = trg.contains(spacelike_edges[0], dim=0).union(trg.contains(spacelike_edges[1], dim=0)).difference({node})

    fut_orig, past_orig = trg.contains(timelike_edges[0], dim=0).union(trg.contains(timelike_edges[1], dim=0)).difference({node})
    past_orig, fut_orig = triangulation_utils.time_order(past_orig, fut_orig, trg)

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
        (simplicial.DimDSimplexKey(spacelike_neighbors.union({fut_orig})), {'s_type': (2, 1), 'dilaton': random.random()}),
        (simplicial.DimDSimplexKey(spacelike_neighbors.union({past_orig})), {'s_type': (1, 2), 'dilaton': random.random()}),
    ]

    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)

    # Meta
    trg.simplex_meta['order'][fut_orig] -= 1
    trg.simplex_meta['order'][past_orig] -= 1


def parity_2d(trg: simplicial.Triangulation, edge: simplicial.DimDSimplexKey):
    """

    Args:
        trg: The triangulation on which to make the move
        edge: a temporal edge that is a member of trg and seperates an up facing from a down facing triangle.

     |\---|       -->     |---/|
     | \  |       -->     |  / |
     |  \ |       -->     | /  |
     |___\|       -->     |/___|

    modifies trg in place by performing a (2,2) type move which modifies a subcomplex of two spatially adjacent triangles in to a subcomplex of 2 triangles.

    This move is described in detail in section 6.3 of "non-perturbative quantum gravity"

    """
    # Discovery
    faces = trg.contains(edge, dim=2)
    nodes = trg.flatten(faces)
    orig_nodes = trg.contains(edge, dim=0)

    fut_orig, past_orig = nodes.difference(orig_nodes)
    fut_edge, past_edge = orig_nodes
    past_orig, fut_orig = triangulation_utils.time_order(fut_orig, past_orig, trg=trg)
    past_edge, fut_edge = triangulation_utils.time_order(fut_edge, past_edge, trg=trg)

    # Remove # TODO simplify this step to not require two loops
    to_remove = {edge}
    for k in range(edge.dim + 1, 2 + 1):  # TODO add a 'dim' attribute to Triangulation
        to_remove = to_remove.union(trg.contains(edge, dim=k))

    for r in to_remove:
        trg.remove_simplex(r)

    # Add
    new_simplices = [
        (simplicial.DimDSimplexKey({fut_orig, past_orig}), {'s_type': (1, 1)}),
        (simplicial.DimDSimplexKey({past_edge, past_orig, fut_orig}), {'s_type': (2, 1), 'dilaton': random.random()}),
        (simplicial.DimDSimplexKey({past_orig, fut_orig, fut_edge}), {'s_type': (1, 2), 'dilaton': random.random()}),
    ]

    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)

    # Meta
    trg.simplex_meta['order'][fut_edge] -= 1
    trg.simplex_meta['order'][past_edge] -= 1
    trg.simplex_meta['order'][fut_orig] += 1
    trg.simplex_meta['order'][past_orig] += 1
