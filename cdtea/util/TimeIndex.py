def time_sep(t1: int, t2: int, time_max: int):
    """ Calculate the separation amount and direction of two time slices"""
    i = (t1 - t2) % time_max
    j = (t2 - t1) % time_max
    if i < j:
        return -i
    if j <= i:
        return j
