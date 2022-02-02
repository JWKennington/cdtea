"""Tests for the simplicial module"""

from cdtea import simplicial, metropolis
from cdtea.tests import admin

from cdtea.generate_flat import generate_flat_2d_space_time

# TODO
"""
Possible things to test for
1. proper random selection
2. proper acceptance ratio

 Not sure how to cover either of these, so im just writing tests that make sure the functions run for now.
"""


class TestMoves2D(admin.CleanScope):
    """Tests for the 2-Dimensional Moves"""

    def test_add_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""
        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        metropolis.add_step(st, lmbda=.1)

    def test_rem_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""
        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        metropolis.add_step(st, lmbda=.1)

    def test_parity_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""
        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        metropolis.parity_step(st)

    def test_step(self):
        """Not sure how to meaningfully test each of these, so im just making sure an example runs."""
        st = generate_flat_2d_space_time(space_size=5, time_size=5)
        metropolis.step(st)
