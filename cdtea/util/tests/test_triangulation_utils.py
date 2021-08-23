import itertools
from collections import defaultdict
import numpy as np
import pytest
from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.util import triangulation_utils as Ordering
from cdtea.simplicial import simplex_key

my_list = [1, 2, 3, 4]


class TestSpatialOrdering:

    def test_get_layer(self):
        """
            for each layer test that it is the correct size
            and that all nodes are contained within two edges.

        """
        st = generate_flat_2d_space_time(space_size=5, time_size=8)

        for t in range(st.time_size):

            layer = Ordering.get_layer(st, t)

            assert len(layer) == 5

            counts = defaultdict(int)
            for pair in itertools.combinations(layer, r=2):
                potential_edge = simplex_key(pair)
                if potential_edge in st.edges:
                    for n in pair:
                        counts[n] += 1

            assert all(value == 2 for value in counts.values())
        with pytest.raises(Exception):
            Ordering.get_layer(st, 1230)
        with pytest.raises(Exception):
            Ordering.get_layer(st, -10)
        with pytest.raises(Exception):
            Ordering.get_layer(st, .74)

    def test_spatial_ordering(self):
        st = generate_flat_2d_space_time(space_size=5, time_size=8)
        for t in range(st.time_size):
            layer = Ordering.get_layer(st, t)
            spatial_order = Ordering.spatial_ordering(st, layer)
            X = len(spatial_order)
            for i, node in enumerate(spatial_order):
                potential_edge = node | spatial_order[(i + 1) % X]
                assert potential_edge in st.edges
                assert st.simplex_meta[potential_edge]["s_type"] == (2, 0)

    def test_get_layer_parity(self):

        st = generate_flat_2d_space_time(space_size=5, time_size=8)
        l1, l2 = Ordering.get_layer(st, 3), Ordering.get_layer(st, 4)
        l1 = Ordering.spatial_ordering(st, l1)
        Ordering.get_layer_parity(l2, l1[0], l1[1], st)
        with pytest.raises(Exception):
            Ordering.get_layer_parity(l2, l1[0], l1[3], st)

    def test_total_ordering(self):
        st = generate_flat_2d_space_time(space_size=7, time_size=5)
        total_ordering = Ordering.total_ordering(st)
        T = st.time_size
        for t in range(T - 1):
            time_edge_1 = total_ordering[t][0] | total_ordering[(t + 1) % T][0]
            assert time_edge_1 in st.edges
            assert st.simplex_meta[time_edge_1]["s_type"] == (1, 1)

            if t % 2 == 0:
                time_edge_2 = total_ordering[t][1] | total_ordering[(t + 1) % T][2]
            else:
                time_edge_2 = total_ordering[t][1] | total_ordering[(t + 1) % T][0]
            assert time_edge_2 in st.edges
            assert st.simplex_meta[time_edge_2]["s_type"] == (1, 1)

    def test_time_sep(self):
        assert Ordering.time_sep(2, 8, 10) == -4
        assert Ordering.time_sep(8, 2, 10) == 4
        assert Ordering.time_sep(8, 8, 10) == 0

    def test_nearest(self):
        """
            for each layer test that it is the correct size
            and that all nodes are contained within two edges.

        """
        ref = np.array([.8, .5]) * 2 * np.pi
        pnt = np.array([.1, .6]) * 2 * np.pi
        result = np.array([1.1, .6]) * 2 * np.pi
        assert np.allclose(Ordering.nearest(ref, pnt), result)

        ref = np.array([.2, .1]) * 2 * np.pi
        pnt = np.array([.9, .8]) * 2 * np.pi
        result = np.array([-.1, -.2]) * 2 * np.pi
        assert np.allclose(Ordering.nearest(ref, pnt), result)
