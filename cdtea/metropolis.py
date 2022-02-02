from cdtea.moves import add_2d, rem_2d, parity_2d
from cdtea import simplicial
import numpy as np


# pg 61,62

def add_step(st: simplicial.Triangulation, lmbda: float) -> bool:
    """

    Args:
        st: the triangulation that is being operated on
        lmbda: The effective cosmological constant

    Returns: a bool representing weather or not the move was accepted

    """
    N = st.num_nodes

    random_spatial_edge = np.random.choice(list(st.spatial_edges))

    acceptance_rate_add = min(1, N / (N + 1) * np.exp(-2 * lmbda))
    if acceptance_rate_add > np.random.random():
        add_2d(st, random_spatial_edge)
        return True
    return False


def rem_step(st: simplicial.Triangulation, lmbda: float) -> bool:
    """

    Args:
        st: the triangulation that is being operated on
        lmbda: The effective cosmological constant

    Returns: a bool representing weather or not the move was accepted

    """
    N = st.num_nodes
    if len(st.rank_4_nodes) > 0:
        random_rank_4_node = np.random.choice(list(st.rank_4_nodes))

        acceptance_rate_add = 1 / (min(1, N / (N + 1) * np.exp(-2 * lmbda)))
        if acceptance_rate_add > np.random.random():
            rem_2d(st, random_rank_4_node)
            return True
    return False


def parity_step(st: simplicial.Triangulation) -> bool:
    """

    Args:
        st: the triangulation that is being operated on

    Returns: a bool representing weather or not the move was accepted

    """
    random_mixed_face_temporal_edge = np.random.choice(list(st.mixed_face_temporal_edges))

    acceptance_rate_add = .5
    if acceptance_rate_add > np.random.random():
        parity_2d(st, random_mixed_face_temporal_edge)
        return True
    return False


def step(st: simplicial.Triangulation, lmbda=np.log(2)):
    """

    Args:
        st:
        lmbda:

    Returns:

    """
    accepted_add = add_step(st=st, lmbda=lmbda)
    accepted_rem = rem_step(st=st, lmbda=lmbda)
    accepted_parity = parity_step(st=st)
    return accepted_add, accepted_rem, accepted_parity
