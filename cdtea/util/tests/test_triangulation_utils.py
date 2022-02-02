"""Test triangulation utils"""
import itertools
from collections import defaultdict
import numpy as np
import pytest
from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.tests import admin
from cdtea.util import triangulation_utils as Ordering
from cdtea.simplicial import simplex_key
from cdtea import simplicial

my_list = [1, 2, 3, 4]


class TestOrdering(admin.CleanScope):
    "test methods for ordering nodes in a triangulation"

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
                assert st.simplex_meta["s_type"][potential_edge] == (2, 0)

    def test_get_layer_parity(self):

        st = generate_flat_2d_space_time(space_size=5, time_size=8)
        l1, l2 = Ordering.get_layer(st, 3), Ordering.get_layer(st, 4)
        l1 = Ordering.spatial_ordering(st, l1)
        Ordering.get_layer_parity(l1, l1[0], l1[1], st)
        with pytest.raises(Exception):
            Ordering.get_layer_parity(l2, l1[0], l1[3], st)

    def test_total_ordering(self):
        """ Test creating a complete ordering of a space_time"""
        st = generate_flat_2d_space_time(space_size=7, time_size=5)
        total_ordering = Ordering.total_ordering(st)
        T = st.time_size
        for t in range(T - 1):
            time_edge_1 = total_ordering[t][0] | total_ordering[(t + 1) % T][0]
            assert time_edge_1 in st.edges
            assert st.simplex_meta["s_type"][time_edge_1] == (1, 1)

            if t % 2 == 0:
                time_edge_2 = total_ordering[t][1] | total_ordering[(t + 1) % T][2]
            else:
                time_edge_2 = total_ordering[t][1] | total_ordering[(t + 1) % T][0]
            assert time_edge_2 in st.edges
            assert st.simplex_meta["s_type"][time_edge_2] == (1, 1)

    def test_time_sep(self):
        assert Ordering.time_sep(2, 8, 10) == -4
        assert Ordering.time_sep(8, 2, 10) == 4
        assert Ordering.time_sep(8, 8, 10) == 0
        with pytest.raises(Exception):
            Ordering.time_sep(.1, .4, 10)

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

    def test_get_shared_future(self):
        """tests get shared_future
        """
        t = simplicial.Triangulation(time_size=2)

        # create some nodes
        n1 = simplicial.Dim0SimplexKey(1)
        n2 = simplicial.Dim0SimplexKey(2)
        n3 = simplicial.Dim0SimplexKey(3)
        n4 = simplicial.Dim0SimplexKey(4)

        # create some edges
        e12 = simplicial.DimDSimplexKey(basis={n1, n2})
        e23 = simplicial.DimDSimplexKey(basis={n2, n3})
        e31 = simplicial.DimDSimplexKey(basis={n3, n1})
        e14 = simplicial.DimDSimplexKey(basis={n1, n4})
        e42 = simplicial.DimDSimplexKey(basis={n4, n2})

        # create some faces
        f1 = simplicial.DimDSimplexKey(basis={n1, n2, n3})
        f2 = simplicial.DimDSimplexKey(basis={n2, n1, n4})

        # add simplices to triangulation
        t.add_simplex(n1, t=2)
        t.add_simplex(n2, t=2)
        t.add_simplex(n3, t=3)
        t.add_simplex(n4, t=1)

        t.add_simplex(e12, edge_type='spatial')
        t.add_simplex(e23, edge_type='spatial')
        t.add_simplex(e14, edge_type='spatial')
        t.add_simplex(e31, edge_type='temporal')
        t.add_simplex(e42, edge_type='temporal')

        t.add_simplex(f1, dilaton=0.5)
        t.add_simplex(f2, dilaton=0.6)

        assert Ordering.get_shared_future(n1, n2, t) == n3
