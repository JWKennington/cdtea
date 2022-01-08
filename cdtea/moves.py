"""Moves

"""
from cdtea import simplicial


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
    orig_layer = trg.simplex_meta['t'][orig_nodes[0]]

    # Remove # TODO simplify this step to not require two loops
    to_remove = set()
    for k in range(edge.dim + 1, 2 + 1)  # TODO add a 'dim' attribute to Triangulation
        to_remove.union(trg.contains(edge, dim=k))

    for r in to_remove:
        trg.remove_simplex(r)

    # Add
    new_vertex = simplicial.Dim0SimplexKey(trg.max_index + 1) # TODO test the new number
    new_simplices = ([(simplicial.DimDSimplexKey({new_vertex, old}), {'type': (2,0)}) for old in orig_nodes] +
                     [(simplicial.DimDSimplexKey({new_vertex, old}), {'type': (1,1)}) for old in nodes.difference(orig_nodes)])
    trg.add_simplex(new_vertex, t=orig_layer)
    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)