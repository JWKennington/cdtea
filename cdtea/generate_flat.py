from cdtea import simplicial
import random


def generate_flat_2d_space_time(T, X):
    st = simplicial.Triangulation()

    def add_simplex(basis, **meta):
        st.add_simplex(simplicial.DimDSimplexKey(basis=basis), **meta)

    def idx(x, t):
        # returns an index in the spacetime, corrects for overflow in space and time
        return (t % T) * X + x % X

    for t in range(T):
        for x in range(X):
            # new vertex (one added per iteration )
            i = idx(x, t)
            add_simplex({i})

            # new edges (three added per vertex)
            spatial_edge_basis = {idx(x, t), idx(t, x + 1)}
            add_simplex(spatial_edge_basis, type=[2, 0])

            past_edge_basis = {idx(x, t), idx(t + 1, x)}
            add_simplex(past_edge_basis, type=[1, 1])

            future_edge_basis = {idx(x, t), idx(t - 1, x - 1)}
            add_simplex(future_edge_basis, type=[1, 1])

            # new triangles (two added per vertex)
            up_triangle_basis = {idx(x, t), idx(x + 1, t), idx(x + 0, t + 1)}
            add_simplex(up_triangle_basis, type=[2, 1], dilaton=random.Random())

            down_triangle_basis = {idx(x, t), idx(x + 1, t), idx(x + 1, t - 1)}
            add_simplex(down_triangle_basis, type=[1, 2], dilaton=random.Random())
    return st
