"""Module for implementing the metropolis steps

References:
    Nonperturbative Quantum Gravity:  	arXiv:1203.3591
    # pg 61,62
"""

from cdtea.moves import add_2d, rem_2d, parity_2d
from cdtea import simplicial
import numpy as np


def add_step(st: simplicial.Triangulation, spatial_edge: simplicial.SimplexKey, lmbda: float) -> bool:
    """

    Args:
        st: the triangulation that is being operated on
        lmbda: The effective cosmological constant

    Returns: a bool representing weather or not the move was accepted

    """
    N = st.num_nodes

    acceptance_rate_add = min(1, N / (N + 1) * np.exp(-2 * lmbda))
    if acceptance_rate_add > np.random.random():
        add_2d(st, spatial_edge)
        return True
    return False


def rem_step(st: simplicial.Triangulation, node: simplicial.DimDSimplexKey, lmbda: float) -> bool:
    """

    Args:
        st: the triangulation that is being operated on
        lmbda: The effective cosmological constant

    Returns: a bool representing weather or not the move was accepted

    """
    N = st.num_nodes

    rem_2d(st, node)
    return True


def parity_step(st: simplicial.Triangulation, edge: simplicial.DimDSimplexKey) -> bool:
    """

    Args:
        st: the triangulation that is being operated on

    Returns: a bool representing weather or not the move was accepted

    """

    parity_2d(st, edge)
    return True
    # return False


def step(st: simplicial.Triangulation, alternation_frequency=.5, lmbda=np.log(2)):
    """

    Args:
        st:
        lmbda:

    Returns:

    """
    if np.random.random() < alternation_frequency:

        random_spatial_edge = np.random.choice(list(st.spatial_edges))
        random_vert = random_spatial_edge.basis_list[0]
        accepted_add = add_step(st=st, spatial_edge=random_spatial_edge, lmbda=lmbda)
        if st.simplex_meta["order"][random_vert] == 4:
            accepted_rem = rem_step(st=st, node=random_vert, lmbda=lmbda)
    else:
        random_mixed_face_temporal_edge = np.random.choice(list(st.mixed_face_temporal_edges))
        accepted_parity = parity_step(st=st, edge=random_mixed_face_temporal_edge)
    # return accepted_add, accepted_rem, accepted_parity
