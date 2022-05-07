"""Module for implementing the metropolis steps

References:
    Nonperturbative Quantum Gravity:  	arXiv:1203.3591
    # pg 61,62
"""

from cdtea.moves import add_2d, rem_2d, parity_2d
from cdtea import simplicial
import numpy as np
import copy


def add_step(st: simplicial.Triangulation, spatial_edge: simplicial.SimplexKey, lmbda: float) -> bool:
    """

    Args:
        st: the triangulation that is being operated on
        lmbda: The effective cosmological constant

    Returns: a bool representing weather or not the move was accepted

    """
    N = st.num_nodes

    # acceptance_rate_add = min(1, N / (N + 1) * np.exp(-2 * lmbda))
    # if acceptance_rate_add > np.random.random():
    add_2d(st, spatial_edge)
    return True
    # return False


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


def step(st: simplicial.Triangulation, action, alternation_frequency=.5, lmbda=np.log(2)):
    """

    Args:
        st:
        lmbda:
        action:
        alternation_frequency:

    Returns:

    """

    """
    "In order to have an ergodic set of moves we will also need to invoke the (2,2)-move, which we will simply do by alternating with a suitable frequency between (2,4)- and (2,2)-moves.
    """
    if np.random.random() < alternation_frequency:
        N = st.num_nodes

        """
        We define the selection probability g(TN0 → TN0+1) to be the same for all triangulations TN0+1 that can be reached in this way and zero for all other labeled TN0+1 triangulations.
        """
        # This effectively implements the g function for the (2,4) move. I.E. uniform probability for any triangulation reached by a (2,4) move
        random_spatial_edge = np.random.choice(list(st.spatial_edges))

        possible_st = copy.deepcopy(st)
        add_step(st=possible_st, spatial_edge=random_spatial_edge, lmbda=lmbda)

        ds = action(possible_st) - action(st)
        # print(ds)
        acceptence_rate_add = np.minimum(1, N / (N + 1) * np.e ** ds)
        if acceptence_rate_add:
            st = possible_st

        """
        Select the vertex labeled N0 + 1, and assume for the moment it is of order four
        """
        # im not sure if this means I should be looking at the same vertex as above?
        # It seems like yes when it is said
        """
        Thus, for the triangulations TN0+1 where the move can be performed we can only reach one triangulation TN0 and the selection probability g(TN0+1 → TN0) defined by this procedure is one.
        """
        # it seems like no when it is said
        """
        Given a labeled triangulation TN0+1 we perform the (4,2)-move as follows. Select the vertex labeled N0 + 1, and assume for the moment it is of order four.
        """
        # This probability further changes based on how we deal with the case when N+1 isnt order 4. If we dont perform the move and move on, or do we randomly select from the list of order 4 verts.

        random_vert = random_spatial_edge.basis_list[0]
        if st.simplex_meta["order"][random_vert] == 4:
            possible_st = copy.deepcopy(st)
            rem_step(st=possible_st, node=random_vert, lmbda=lmbda)
            ds = action(possible_st) - action(st)
            acceptence_rate_rem = np.minimum(1, (N + 1) / N * np.e ** (-ds))
            if np.random.random() < acceptence_rate_rem:
                st = possible_st

    else:
        N = st.num_nodes
        possible_st = copy.deepcopy(st)
        random_mixed_face_temporal_edge = np.random.choice(list(st.mixed_face_temporal_edges))
        parity_step(st=possible_st, edge=random_mixed_face_temporal_edge)
        ds = action(possible_st) - action(st)

        acceptence_rate_rem = np.minimum(1, (N + 1) / N * np.e ** (-ds))
        if np.random.random() < acceptence_rate_rem:
            st = possible_st

    return st
