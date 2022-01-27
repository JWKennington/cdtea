"""tests for the generation of coordinates for triangulations"""

from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.Visualization.coordinates import toroidal_coordinates


class TestCoordinates:
    """tests for the generation of coordinates for triangulations"""

    def test_toroidal_coordinates(self):
        """
            Test that toroidal_coordinates is properly outputting tuples of floats.
        """
        st = generate_flat_2d_space_time(space_size=5, time_size=8)
        coords = toroidal_coordinates(st)
        for c in coords.values():
            assert isinstance(c, tuple)
            assert isinstance(c[0], float)
            assert isinstance(c[1], float)
