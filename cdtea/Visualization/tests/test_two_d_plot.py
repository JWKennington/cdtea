"""Test 2d plotting"""
from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.Visualization.two_d_plot import two_d_plot


class TestTwoDPlot:
    """Test 2d plotting"""

    def test_run(self):
        """This test makes sure that generate_flat creates a triangulation
        """

        st = generate_flat_2d_space_time(7, 9)
        two_d_plot(st)
