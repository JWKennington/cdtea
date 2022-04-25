"""Tests for the simplicial module"""

from cdtea import metropolis

from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea import moves

"""
Possible things to test for
1. proper random selection
2. proper acceptance ratio

 Not sure how to cover either of these, so im just writing tests that make sure the functions run for now.
"""


class TestMoves2D:
    """Tests for the 2-Dimensional Moves"""

    def test_add_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""
        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        spatial_edge = list(st.spatial_edges)[0]
        metropolis.add_step(st, spatial_edge=spatial_edge, lmbda=.1)

    def test_rem_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""
        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        spatial_edge = list(st.spatial_edges)[0]
        moves.add_2d(st,spatial_edge)
        vert = list(st.rank_4_nodes)[0]
        metropolis.rem_step(st, node=vert, lmbda=.1)

    def test_parity_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""
        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        mixedfaceedge = list(st.mixed_face_temporal_edges)[0]
        metropolis.parity_step(st, edge=mixedfaceedge)

    def test_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""

        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        metropolis.step(st)

# random_spatial_edge = np.random.choice(list(st.spatial_edges))
#         random_vert = random_spatial_edge.basis_list[0]
#         accepted_add = add_step(st=st, spatial_edge=random_spatial_edge, lmbda=lmbda)
#         if st.simplex_meta["order"][random_vert] == 4:
#             accepted_rem = rem_step(st=st, node=random_vert, lmbda=lmbda)
#     else:
#         random_mixed_face_temporal_edge = np.random.choice(list(st.mixed_face_temporal_edges))
#         accepted_parity = parity_step(st=st, edge=random_mixed_face_temporal_edge)
