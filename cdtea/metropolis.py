from cdtea.moves import add_2d, rem_2d, parity_2d
from cdtea import simplicial
import numpy as np
from cdtea.Visualization import two_d_plot
from cdtea.tests import valid_triangulation
np.random.seed(1)
# pg 61,62

def add_step(st: simplicial.Triangulation, lmbda: float):
    N = st.num_nodes

    random_spatial_edge = np.random.choice(list(st.spatial_edges))

    acceptance_rate_add = min(1, N / (N + 1) * np.exp(-2 * lmbda))
    if acceptance_rate_add > np.random.random():
        add_2d(st, random_spatial_edge)


def rem_step(st: simplicial.Triangulation, lmbda: float):
    N = st.num_nodes
    if len(st.rank_4_nodes) > 0:
        random_rank_4_node = np.random.choice(list(st.rank_4_nodes))

        acceptance_rate_add = 1 / (min(1, N / (N + 1) * np.exp(-2 * lmbda)))
        if acceptance_rate_add > np.random.random():
            rem_2d(st, random_rank_4_node)


def parity_step(st: simplicial.Triangulation, lmbda: float):
    N = st.num_nodes

    random_mixed_face_temporal_edge = np.random.choice(list(st.mixed_face_temporal_edges))

    acceptance_rate_add = .5
    if acceptance_rate_add > np.random.random():
        parity_2d(st, random_mixed_face_temporal_edge)


def step(st: simplicial.Triangulation, lmbda=np.log(2)):
    """

    Args:
        st:
        lmbda:

    Returns:

    """
    add_step(st=st, lmbda=lmbda)
    rem_step(st=st, lmbda=lmbda)
    parity_step(st=st, lmbda=lmbda)


import generate_flat

st = generate_flat.generate_flat_2d_space_time(8, 8)

for i in range(100):
    print(i)
    step(st)
import matplotlib.pyplot as plt
valid_triangulation.is_valid(st)
two_d_plot.two_d_plot(st)
plt.show()
