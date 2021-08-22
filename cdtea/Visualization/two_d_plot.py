from cdtea.Visualization.coordinates import toroidal_coordinates, nearest
from cdtea.generate_flat import generate_flat_2d_space_time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection
from cdtea.simplicial import Triangulation
import collections


def two_d_plot(st: Triangulation, display: bool = True):
    ax = plt.gca()
    meta = st.simplex_meta
    coordinates = toroidal_coordinates(st)

    # plot the points
    X, Y, pnt_colors = [], [], []
    edge_color = collections.defaultdict(int)
    for e in st.edges:
        for v in e:
            edge_color[v] += 1
    for v in coordinates:
        X.append(coordinates[v][0])
        Y.append(coordinates[v][1])
        c_index = (edge_color[v] - 5.) / 7.
        pnt_colors.append((c_index, 0, 1 - c_index, 1))

    ax.scatter(X, Y, c=pnt_colors, s=100)

    # plot all the edges
    lines, line_colors = [], []
    for e in st.edges:
        b = e.basis_list
        delta_t = abs(meta[b[0]]["t"] - meta[b[1]]["t"])
        if delta_t == 0 or delta_t == 1:
            pts = np.array([coordinates[v] for v in e])
            pts = np.array([nearest(np.max(pts, 0), p) for p in pts])
            center = np.mean(pts, 0)
            pts = (pts - center) / 1.8 + center
            lines.append(pts)
            color = 'b'
            if meta[e]['s_type'] == (2, 0):
                color = 'r'
            line_colors.append(color)
    lc = LineCollection(lines, colors=line_colors)
    ax.add_collection(lc)

    # faces
    for s in st.faces:
        # check that this face isnt in the cut region
        if all([all([abs(meta[v1]["t"] - meta[v2]["t"]) < 2 for v2 in s]) for v1 in s]):
            pts = np.array([coordinates[v] for v in s])
            pts = np.array([nearest(np.max(pts, 0), p) for p in pts])
            center = np.mean(pts, 0)
            pts = (pts - center) / 1.8 + center
            color = (0, 0, 1, .5)
            if meta[s]["s_type"] == (2, 1):
                color = (1, 0, 0, .5)
            p = Polygon(pts, closed=False, color=color)
            ax.add_patch(p)
    if display:
        plt.show()
