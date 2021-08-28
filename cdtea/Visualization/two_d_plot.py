""" plotting functions for 2d space-times with toroidal topology"""

import collections
from cdtea.Visualization.coordinates import toroidal_coordinates
from cdtea.util.triangulation_utils import nearest
from cdtea.simplicial import Triangulation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection


def two_d_plot(st: Triangulation) -> type(plt.gca()):
    """create a matplotlib ax"""
    ax = plt.gca()
    meta = st.simplex_meta
    coordinates = toroidal_coordinates(st)

    plot_points(ax, coordinates, st)

    plot_edges(ax, coordinates, meta, st)

    plot_faces(ax, coordinates, meta, st)

    return ax


def plot_faces(ax, coordinates, meta, st):
    """plot the faces"""
    for s in st.faces:
        # check that this face isnt in the cut region
        def t_param_difference(v1, v2):
            return abs(meta["t"][v1] - meta["t"][v2])

        if all(all(t_param_difference(v1, v2) < 2 for v2 in s) for v1 in s):
            pts = np.array([coordinates[v] for v in s])
            pts = np.array([nearest(np.max(pts, 0), p) for p in pts])
            center = np.mean(pts, 0)
            pts = (pts - center) / 1.8 + center
            color = (0, 0, 1, .5)
            if meta["s_type"][s] == (2, 1):
                color = (1, 0, 0, .5)
            p = Polygon(pts, closed=False, color=color)
            ax.add_patch(p)


def plot_points(ax, coordinates, st):
    """plot the points"""
    X, Y, pnt_colors = [], [], []
    edge_color = collections.defaultdict(int)
    for e in st.edges:
        for v in e:
            edge_color[v] += 1
    for v,c in coordinates.items():
        X.append(c[0])
        Y.append(c[1])
        c_index = (edge_color[v] - 5.) / 7.
        pnt_colors.append((c_index, 0, 1 - c_index, 1))
    ax.scatter(X, Y, c=pnt_colors, s=100)


def plot_edges(ax, coordinates, meta, st):
    """plot the edges"""
    lines, line_colors = [], []
    for e in st.edges:
        b = e.basis_list
        delta_t = abs(meta["t"][b[0]] - meta["t"][b[1]])
        if delta_t in (0, 1):
            pts = np.array([coordinates[v] for v in e])
            pts = np.array([nearest(np.max(pts, 0), p) for p in pts])
            center = np.mean(pts, 0)
            pts = (pts - center) / 1.8 + center
            lines.append(pts)
            color = 'b'
            if meta['s_type'][e] == (2, 0):
                color = 'r'
            line_colors.append(color)
    lc = LineCollection(lines, colors=line_colors)
    ax.add_collection(lc)
