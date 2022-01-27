def torus_sep(point1, point2):
    xdiff = abs(point1[0] - point2[0])
    if xdiff > (1 / 2.):
        xdiff = 1 - xdiff

    ydiff = abs(point1[1] - point2[1])
    if ydiff > (1 / 2.):
        ydiff = 1 - ydiff

    return xdiff, ydiff
