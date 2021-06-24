from cdtea.Visualization.SpatialOrdering import spatial_ordering
from cdtea.simplicial import Triangulation
import numpy as np


def toroidal_coordinates(st: Triangulation):
    meta = st.simplex_meta
    nodes = st.simplices[0]
    edges = st.simplices[1]
    T = st.time_size
    layers = {t: [n for n in nodes if meta[n]['t'] == t] for t in range(T)}
    base_order = spatial_ordering(st, layers[0])
    prev_order = base_order[0:2]
    total_order = [base_order]
    for t in range(1, T):
        layer = layers[t]
        L = len(layer)
        for i in range(len(layer)):
            if ((layer[i] | prev_order[0]) in edges) and ((layer[i] | prev_order[1]) in edges):
                middle = layer[i]
            elif (layer[i] | prev_order[1]) in edges:
                right = layer[i]
            elif (layer[i] | prev_order[0]) in edges:
                left = layer[i]
        if t % 2 == 0:
            ORD = spatial_ordering(st, layers[t], indexed=[middle, right])
        else:
            ORD = spatial_ordering(st, layers[t], indexed=[left, middle])
        prev_order = ORD[0:2]
        total_order.append(ORD)

    coords = {}
    for t, layer in enumerate(total_order):
        for x, v in enumerate(layer):
            L = len(layer)
            # coords[v] = [x - 1./2.*(t%2), sqrt(3)/2.*t]
            coords[v] = [(x - .5 * (t % 2)) / L * 2 * np.pi, t / T * 2 * np.pi]
    return coords
    # print(spatial_ordering(st, layers[t], indexed=))


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
