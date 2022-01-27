""" plotting functions for 2d space-times with toroidal topology"""

import collections
from cdtea.Visualization.coordinates import toroidal_coordinates
from cdtea.util.triangulation_utils import nearest
from cdtea.simplicial import Triangulation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection
from cdtea.Visualization.torus_utils import torus_sep


def relative_point(pnt_a, pnt_b):
    return pnt_a + torus_sep(pnt_a, pnt_b)


def two_d_plot(st: Triangulation) -> type(plt.gca()):
    """create a matplotlib ax"""
    ax = plt.gca()
    meta = st.simplex_meta
    coordinates = toroidal_coordinates(st)

    plt.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        left=False,
        right=False,
        labelleft=False,
        labelbottom=False)  # labels along the bottom edge are off

    plt.xlim([0, 1])
    plt.ylim([0, 1])
    # plt.axis('off')
    ax.set_aspect(1)
    # plot_faces(ax, coordinates, meta, st)
    #
    plot_edges(ax, coordinates, meta, st)
    #
    # plot_points(ax, coordinates, st)

    return ax


def plot_faces(ax, coordinates, meta, st):
    """plot the faces"""
    for s in st.faces:
        # check that this face isnt in the cut region

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # if all(all(t_param_difference(v1, v2) < 2 for v2 in s) for v1 in s):
                pts = np.array([coordinates[v] for v in s])
                # pts = np.array([nearest(np.max(pts, 0), p) for p in pts])
                center = np.mean(pts, 0)

                pts[1] = relative_point(pts[0], pts[1])
                pts[2] = relative_point(pts[0], pts[2])

                pts = pts + np.array([dx, dy])
                # pts = (pts - center) / 1.3 + center
                color = (0, 0, 1, .5)
                if meta["s_type"][s] == (2, 1):
                    color = (1, 0, 0, .5)
                p = Polygon(pts, closed=True, color=color, zorder=0, linewidth=None, fill=None)
                ax.add_patch(p)


def plot_points(ax, coordinates, st):
    """plot the points"""
    X, Y, pnt_colors = [], [], []
    edge_color = collections.defaultdict(int)
    for e in st.edges:
        for v in e:
            edge_color[v] += 1
    for v, c in coordinates.items():
        X.append(c[0])
        Y.append(c[1])
        c_index = (edge_color[v] - 2.) / 100.

        pnt_colors.append((c_index, 0, 1 - c_index, 1))
    ax.scatter(X, Y, c='k', s=10, zorder=2)


def plot_edges(ax, coordinates, meta, st):
    """plot the edges"""
    lines, line_colors = [], []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for e in st.edges:
                pts = np.array([coordinates[v] for v in e])
                center = np.mean(pts, 0)
                # pts = (pts - center) / 1.3 + center
                pts[1] = relative_point(pts[0], pts[1])
                pts = pts + np.array([dx, dy])
                lines.append(pts)
                color = 'b'
                if meta['s_type'][e] == (2, 0):
                    color = 'r'
                line_colors.append(color)
            lc = LineCollection(lines, colors=line_colors, linewidths=.8, zorder=0)
            ax.add_collection(lc)
