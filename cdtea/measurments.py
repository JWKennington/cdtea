"""
This is where all measurements should be defined. A measurement takes in a triangulation and returns some interesting property
"""
from cdtea.simplicial import Triangulation


def volume(st: Triangulation):
    return st.num_nodes


def volume_profile(st: Triangulation):
    return [len(st.simplex_meta['t'].dual[t]) for t in range(st.time_size)]
