from cdtea.Visualization.SpatialOrdering import spatial_ordering, total_ordering
from cdtea.simplicial import Triangulation
import numpy as np


def toroidal_coordinates(st: Triangulation):
    """
    Generate a dict from node -> (theta,phi)

    """
    total_order = total_ordering(st)

    coords = {}
    for t, layer in enumerate(total_order):
        L = len(layer)
        for x, v in enumerate(layer):
            theta = (x - .5 * (t % 2)) / L * 2 * np.pi
            phi = t / st.time_size * 2 * np.pi
            coords[v] = (theta, phi)
    return coords


def nearest(ref, pnt):
    deltas = np.array([[0, 1], [1, 0], [1, 1], [0, -1], [-1, 0], [-1, -1]]) * 2 * np.pi
    sep = np.linalg.norm(pnt - ref)
    final_delta = np.array([0, 0])
    for delta in deltas:
        test_sep = np.linalg.norm(pnt + delta - ref)
        if test_sep < sep:
            sep = test_sep
            final_delta = delta
    return pnt + final_delta
