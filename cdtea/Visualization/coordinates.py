"""
functions for generating coordinates for each 0d vertex in a triangulation
"""

from cdtea.util.triangulation_utils import total_ordering
from cdtea.simplicial import Triangulation


def toroidal_coordinates(st: Triangulation):
    """
    Generate a dict from node -> (theta,phi)

    """
    total_order = total_ordering(st)
    coords = {}
    for t, layer in enumerate(total_order):
        L = len(layer)
        for x, v in enumerate(layer):
            theta = (x - .5 * (t % 2)) / L + .75 / L
            T = st.time_size
            phi = t / T + .5 / T
            coords[v] = (theta, phi)
    return coords
