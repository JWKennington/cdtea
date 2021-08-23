from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.Visualization.coordinates import toroidal_coordinates
import numpy as np


class TestSpatialOrdering:

    def test_toroidal_coordinates(self):
        """
            Test that toroidal_coordinates is properly outputting tuples of floats.
        """
        st = generate_flat_2d_space_time(space_size=5, time_size=8)
        coords = toroidal_coordinates(st)
        for c in coords:
            assert type(coords[c]) is tuple
            assert type(coords[c][0]) is float
            assert type(coords[c][1]) is float


