"""Tests the different moves that can be done to a triangulation"""
import pytest
from cdtea import modifications
from cdtea.simplicial import simplex_key
from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.tests import valid_triangulation as validity


class TestModifications:
    """Tests the different moves that can be done to a triangulation"""

    def test_parity(self):
        """test parity move"""
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)
        key1 = simplex_key({1, 21, 22})
        key2 = simplex_key({1, 2, 22})
        key3 = simplex_key({1, 8, 22})
        key4 = simplex_key({8, 21, 22})

        modifications.parity_move(tri, key1, key2)
        validity.is_valid(tri)
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)

        with pytest.raises(Exception):
            modifications.parity_move(tri, key1, key3)

        with pytest.raises(Exception):
            modifications.parity_move(tri, key1, key4)

    def test_increase(self):
        """test increase move"""
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)
        key1 = simplex_key({10, 6, 5})
        key2 = simplex_key({1, 6, 5})
        modifications.increase_move(tri, key1, key2)
        validity.is_valid(tri)
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)

        with pytest.raises(Exception):
            modifications.increase_move(tri, key1, key1)

        with pytest.raises(Exception):
            key2 = simplex_key({1, 7, 3})
            modifications.increase_move(tri, key1, key2)

    def test_decrease(self):
        """test decrease move"""
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)
        key1 = simplex_key({10, 6, 5})
        key2 = simplex_key({1, 6, 5})
        modifications.increase_move(tri, key1, key2)
        modifications.decrease_move(tri, simplex_key(25))
        validity.is_valid(tri)

        with pytest.raises(Exception):
            tri = generate_flat_2d_space_time(space_size=5, time_size=5)
            key1 = simplex_key({10, 6, 5})
            key2 = simplex_key({1, 6, 5})
            modifications.increase_move(tri, key1, key2)
            modifications.decrease_move(tri, simplex_key(20))
            validity.is_valid(tri)
