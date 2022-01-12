from cdtea import simplicial
from cdtea.util import triangulation_utils as util


def parity_2D(trg: simplicial.Triangulation, edge: simplicial.SimplexKey):
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

    fut_orig, past_orig = orig_nodes
    if util.time_sep(trg.simplex_meta['t'][past_orig], trg.simplex_meta['t'][fut_orig], trg.time_size):
        fut_orig, past_orig = past_orig, fut_orig

    # Remove #
    to_remove = {*faces}
    to_remove.add(edge)

    for r in to_remove:
        trg.remove_simplex(r)

    for node in edge:
        trg.simplex_meta['order'][node] -= 1

    # Add
    new_edge = simplicial.DimDSimplexKey(nodes - orig_nodes)

    new_simplices = [(new_edge, {'s_type': (1, 1)})]
    new_simplices.append((new_edge | past_orig, {'s_type': (1, 2)}))
    new_simplices.append((new_edge | fut_orig, {'s_type': (2, 1)}))

    for new, kwargs in new_simplices:
        trg.add_simplex(new, **kwargs)

    for node in new_edge:
        trg.simplex_meta['order'][node] += 1
