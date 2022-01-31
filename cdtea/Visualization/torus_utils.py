import numpy as np


def torus_sep(point1, point2):
    """

    Args:
        point1: a list of coords each between 0,1
        point2: a list of coords each between 0,1

    Returns: the shortest vector pointing from point1 to point2 in toroidal space, normed so x and y max are 1.

    """
    xdiff = point2[0] - point1[0]
    if abs(xdiff) > (1 / 2.):
        xdiff = xdiff - np.sign(xdiff)

    ydiff = point2[1] - point1[1]
    if abs(ydiff) > (1 / 2.):
        ydiff = ydiff - np.sign(ydiff)

    return xdiff, ydiff
