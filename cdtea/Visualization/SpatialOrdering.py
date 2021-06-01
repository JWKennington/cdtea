from cdtea.simplicial import Dim0SimplexKey, Triangulation


def spatial_ordering(st: Triangulation, layer: list[Dim0SimplexKey], origin: Dim0SimplexKey = None):
    """
    returns a dictionary where each Dim0SimplexKey in layer is mapped to an index.

    note that there are two valid orderings 01234 or 43210
    """

    # if origin is unspecified chose a random origin
    if origin is None:
        origin = layer[0]
    index = {origin: 0}

    # the current "edge" of the ordering
    boundary = origin

    # all nodes that are not yet indexed
    not_indexed = set(layer) - {origin}

    # each iteration adds one new node to the index dict. therefore we need to loop once for each item in layer
    for i in range(len(layer)):

        # for each link in the chain we want to find an item which is connected to the boundary and not yet indexed
        for f in not_indexed:
            if (f | boundary) in st.simplices[1]:
                # remove f from not_indexed
                not_indexed -= {f}
                index[f] = index[boundary] + 1
                boundary = f

                # once one has been found we can move on to the next loop
                break
    return index
