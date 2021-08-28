"""Tests for generating a flat toroidal 2d simplicial manifold"""
from collections import defaultdict
from cdtea import simplicial
from cdtea import generate_flat
from cdtea.tests.valid_triangulation import is_valid
from cdtea.util.triangulation_utils import time_sep


class TestGenerateFlat:
    """Tests for generating a flat toroidal 2d simplicial manifold"""

    def test_create(self):
        """This test makes sure that generate_flat creates a triangulation
        """
        t = generate_flat.generate_flat_2d_space_time(time_size=3, space_size=3)

        assert isinstance(t, simplicial.Triangulation)

    def test_validity(self):
        t = generate_flat.generate_flat_2d_space_time(time_size=5, space_size=5)
        is_valid(t)

    def test_6_super_edges(self):
        """Test that each 0-simplex is contained in 6 edges"""
        t = generate_flat.generate_flat_2d_space_time(time_size=3, space_size=3)
        counts = defaultdict(int)
        for edge in t.edges:
            b = edge.basis_list
            counts[b[0]] += 1
            counts[b[1]] += 1
        # solidify the dictionary
        counts = dict(counts)
        for v in t.nodes:
            assert counts[v] == 6

    def test_6_super_triangles(self):
        """Test that each 0-simplex is contained in 6 triangles"""
        t = generate_flat.generate_flat_2d_space_time(time_size=3, space_size=3)
        counts = defaultdict(int)
        for tri in t.simplices[2]:
            b = tri.basis_list
            counts[b[0]] += 1
            counts[b[1]] += 1
            counts[b[2]] += 1
        # solidify the dictionary
        counts = dict(counts)
        for v in t.nodes:
            assert counts[v] == 6

    # split in to two for past and future edges?
    def test_4_temporal_edges(self):
        """Test that each 0-simplex is contained in 6 edges"""
        t = generate_flat.generate_flat_2d_space_time(time_size=3, space_size=3)
        counts = defaultdict(int)
        for edge in t.edges:
            b = edge.basis_list
            if t.simplex_meta["s_type"][edge] == (1, 1):
                counts[b[0]] += 1
                counts[b[1]] += 1
        # solidify the dictionary
        counts = dict(counts)
        for v in t.nodes:
            assert counts[v] == 4

    def test_correct_size(self):
        """Test that generate_flat_2d_space_time(T,X) has T*X 0-simplices and 3*T*X 1-simplices"""
        space_sizes_to_test = [3, 4, 5, 6]
        time_sizes_to_test = [3, 4, 5, 6]
        for t_size in time_sizes_to_test:
            for x_size in space_sizes_to_test:
                n = t_size * x_size
                t = generate_flat.generate_flat_2d_space_time(time_size=t_size, space_size=x_size)
                assert len(t.nodes) == n
                assert len(t.edges) == 3 * n

    def test_time_index(self):
        """
        Make sure all spatial adjacent nodes have the same t and all time adjacent node have t's that differ by one
        """
        st = generate_flat.generate_flat_2d_space_time(time_size=5, space_size=5)

        def get_type(simplex):
            return st.simplex_meta["s_type"][simplex]

        def get_t(simplex):
            return st.simplex_meta["t"][simplex]

        for edge in st.edges:
            lst = edge.basis_list
            if get_type(edge) == (1, 1):
                assert abs(time_sep(get_t(lst[0]), get_t(lst[1]), st.time_size)) == 1
            elif get_type(edge) == (2, 0):
                assert get_t(lst[0]) == get_t(lst[1])
            else:
                raise Exception(f"edge {edge} has invalid type {get_type(edge)}")
