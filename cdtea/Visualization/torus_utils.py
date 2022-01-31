def torus_sep(point1, point2):
    """

    Args:
        point1: a list of coords each between 0,1
        point2: a list of coords each between 0,1

    Returns: the shortest vector pointing from point1 to point2 in toroidal space, normed so x and y max are 1.

    """
    xdiff = abs(point1[0] - point2[0])
    if xdiff > (1 / 2.):
        xdiff = 1 - xdiff

    ydiff = abs(point1[1] - point2[1])
    if ydiff > (1 / 2.):
        ydiff = 1 - ydiff

    return xdiff, ydiff
