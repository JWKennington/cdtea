"""
Function to generate an initial simplicial manifold that is flat, with toroidal topology.
"""

from __future__ import annotations

import random
from typing import Union, List, Tuple

from cdtea import simplicial


def generate_flat_2d_space_time(time_size: int, space_size: int) -> simplicial.Triangulation:
    """
    returns a flat 2d simplicial.Triangulation with toroidal topology consisting of
    n 0-simplices, 3n 1-simplices, and 2n 2-simplices
    where n = time_size*space_size.

    Each simplex is instantiated with a "s_type" metadata with the convention being
    s_type = (number of constituent 0-simplices in past, number of constituent 0-simplices in future)
    0-simplices are not given a s_type because they all have the same type.
    0-simplices are instantiated with a "t" metadata value which is a time index.
    2-simplices are instantiated with a "dilaton" metadata value, which is random.

    time_size: an int specifying the number of space-like slices in the triangulation
    space_size: an int specifying the resolution of each space-like slice

    """
    space_time = simplicial.Triangulation(time_size=time_size)

    def add_simplex(basis: Union[set, int], **meta):
        """shorthand for adding a simplex to the triangulation"""
        if isinstance(basis, int):
            space_time.add_simplex(simplicial.Dim0SimplexKey(key=basis), **meta)
        else:
            basis = {simplicial.Dim0SimplexKey(key=b) for b in basis}
            space_time.add_simplex(simplicial.DimDSimplexKey(basis=basis), **meta)

    def idx(x_idx: int, t_idx: int):
        """shorthand for returning a unique index for a given space-time position.
        It autocorrects for space and time overflow
        """
        return (t_idx % time_size) * space_size + x_idx % space_size

    for t in range(time_size):
        for x in range(space_size):
            # new vertex (one added per iteration )
            i = idx(x_idx=x, t_idx=t)
            add_simplex(i, t=t, order=6)

    for t in range(time_size):
        for x in range(space_size):
            # new edges (three added per vertex)
            spatial_edge_basis = {idx(x_idx=x, t_idx=t), idx(x_idx=x + 1, t_idx=t)}
            add_simplex(spatial_edge_basis, s_type=(2, 0))

            past_edge_basis = {idx(x_idx=x, t_idx=t), idx(x_idx=x, t_idx=t + 1)}
            add_simplex(past_edge_basis, s_type=(1, 1))

            future_edge_basis = {idx(x_idx=x, t_idx=t), idx(x_idx=x - 1, t_idx=t + 1)}
            add_simplex(future_edge_basis, s_type=(1, 1))
    for t in range(time_size):
        for x in range(space_size):
            # new triangles (two added per vertex)
            # each triangle is instantiated with a random dilaton value between zero and 1 using random.Random()
            up_triangle_basis = {idx(x_idx=x, t_idx=t), idx(x_idx=x + 1, t_idx=t), idx(x_idx=x + 0, t_idx=t + 1)}
            add_simplex(up_triangle_basis, s_type=(2, 1), dilaton=random.Random())

            down_triangle_basis = {idx(x_idx=x, t_idx=t + 1), idx(x_idx=x + 1, t_idx=t + 1), idx(x_idx=x + 1, t_idx=t)}
            add_simplex(down_triangle_basis, s_type=(1, 2), dilaton=random.Random())
    return space_time


def generate(nodes: List[int], simplices: List[Tuple[int, ...]], node_layers: List[int]) -> simplicial.Triangulation:
    """General CDT generation utility. Given a set of nodes, the corresponding time indices,
    and the edges connecting them, create a Triangulation instance with all meta data
    properly inferred from the given DOT compliant graph structure.

    Args:
        nodes:
            List[int], list of node labels
        simplices:
            List[Tuple[int, ...]], list of dim = k > 0 simplices specified by a tuple of (node1, ..., nodek), where
            the tuple of nodes represents the basis of the simplex
        node_layers:
            List[int], a list of the time indices of the nodes. Must have the same size as the
            nodes argument, and the order must correspond to the order in the nodes argument.

    Returns:
        Triangulation
    """
    raise NotImplementedError
