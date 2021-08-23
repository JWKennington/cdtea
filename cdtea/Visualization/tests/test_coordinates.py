from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.Visualization.coordinates import toroidal_coordinates, nearest
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

    def test_nearest(self):
        """
            for each layer test that it is the correct size
            and that all nodes are contained within two edges.

        """
        ref = np.array([.8, .5]) * 2 * np.pi
        pnt = np.array([.1, .6]) * 2 * np.pi
        result = np.array([1.1, .6]) * 2 * np.pi
        assert np.allclose(nearest(ref, pnt), result)

        ref = np.array([.2, .1]) * 2 * np.pi
        pnt = np.array([.9, .8]) * 2 * np.pi
        result = np.array([-.1, -.2]) * 2 * np.pi
        assert np.allclose(nearest(ref, pnt), result)
