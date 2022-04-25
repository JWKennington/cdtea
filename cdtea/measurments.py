"""
This is where all measurements should be defined. A measurement takes in a triangulation and returns some interesting property
"""
import numpy as np
from cdtea.simplicial import Triangulation


def take_measurements(st: Triangulation, measurements: list):
    return [measurement(st) for measurement in measurements]


def volume(st: Triangulation):
    return st.num_nodes


def volume_profile(st: Triangulation):
    return [len(st.simplex_meta['t'].dual[t]) for t in range(st.time_size)]


def average_length(st: Triangulation):
    return np.mean(volume_profile(st))
