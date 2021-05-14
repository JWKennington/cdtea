from cdtea import modifications
from cdtea.simplicial import simplex_key
from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.tests import valid_triangulation as validity


class TestModifications:

    def test_parity(self):
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)
        key1 = simplex_key({1, 21, 22})
        key2 = simplex_key({1, 2, 22})
        modifications.parity_move(tri, key1, key2)
        validity.is_valid(tri)

    def test_increase(self):
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)
        key1 = simplex_key({10, 6, 5})
        key2 = simplex_key({1, 6, 5})
        modifications.increase_move(tri, key1, key2)
        validity.is_valid(tri)

    def test_decrease(self):
        tri = generate_flat_2d_space_time(space_size=5, time_size=5)
        key1 = simplex_key({10, 6, 5})
        key2 = simplex_key({1, 6, 5})
        modifications.increase_move(tri, key1, key2)
        modifications.decrease_move(tri, simplex_key(25))
        validity.is_valid(tri)
