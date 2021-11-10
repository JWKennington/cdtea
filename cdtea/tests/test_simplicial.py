"""Tests for the simplicial module"""

from cdtea import simplicial
import pytest


class TestTriangulation:
    """Tests for the Triangulation Class"""

    def test_create(self):
        """This test serves as an initial test of adding simplices to a triangulation
        There are many intermediate steps that can be simplified and validity checks
        for simplices that can be added
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
        e34 = simplicial.DimDSimplexKey(basis={n3, n4})
        e42 = simplicial.DimDSimplexKey(basis={n4, n2})

        # create some faces
        f1 = simplicial.DimDSimplexKey(basis={n1, n2, n3})
        f2 = simplicial.DimDSimplexKey(basis={n2, n3, n4})

        # add simplices to triangulation
        t.add_simplex(n1)
        t.add_simplex(n2)
        t.add_simplex(n3)
        t.add_simplex(n4)

        t.add_simplex(e12, edge_type='spatial')
        t.add_simplex(e23, edge_type='spatial')
        t.add_simplex(e34, edge_type='spatial')
        t.add_simplex(e31, edge_type='temporal')
        t.add_simplex(e42, edge_type='temporal')

        t.add_simplex(f1, dilaton=0.5)
        t.add_simplex(f2, dilaton=0.6)

        assert isinstance(t, simplicial.Triangulation)

    def test_equality(self):
        t1, t2 = simplicial.Triangulation(time_size=2), simplicial.Triangulation(time_size=2)
        t3 = simplicial.Triangulation(time_size=3)
        assert t1 == t2
        assert t1 != t3
        assert t1 != 7

    def test_remove_simplex(self):
        """we cant compare to a fresh triangulation becouse we are using default dict and once a value is added it remembers that there is a category for that dimension"""
        t1 = simplicial.Triangulation(time_size=2)
        t2 = simplicial.Triangulation(time_size=2)
        t1.add_simplex(simplicial.simplex_key({1, 2, 3}), prop="test meta property")
        t1.remove_simplex(simplicial.simplex_key({1, 2, 3}))
        t2.add_simplex(simplicial.simplex_key({1, 4, 3}), prop="test meta property")
        t2.remove_simplex(simplicial.simplex_key({1, 4, 3}))
        assert t1 == t2

    def test_sub_simplex(self):
        """test that the sub_simplex method returns the correct simplices"""
        s = simplicial.simplex_key({1, 2, 3})
        tri = simplicial.Triangulation(time_size=2)
        tri.add_simplex(s, prop="test meta property")
        k = simplicial.simplex_key
        v1, v2, v3 = s.basis_list
        expected = {v1, v2, v3, k({v1, v2}), k({v1, v3}), k({v2, v3})}
        assert tri.simplex_meta['contains'][s] == expected

    def test_rank_4(self):
        """test that the rank_4_nodes method gives the correct output"""
        n1 = simplicial.simplex_key({1})
        n2 = simplicial.simplex_key({2})

        tri = simplicial.Triangulation(time_size=2)

        tri.add_simplex(n1, order=4)
        tri.add_simplex(n2, order=2)

        assert tri.rank_4_nodes == {n1}

    def test_spatial_edges(self):
        """test that the spatial_edges method gives the correct output"""

        e1 = simplicial.simplex_key({1, 2})
        e2 = simplicial.simplex_key({1, 10})

        tri = simplicial.Triangulation(time_size=2)

        tri.add_simplex(e1, s_type=(2, 0))
        tri.add_simplex(e2, s_type=(1, 1))

        assert tri.spatial_edges == {e1}


class TestSimplexKey:
    """Tests for the SimplexKey Classes"""

    def test_create_dim_0_simplex_key(self):
        simplicial.Dim0SimplexKey(1)
        simplicial.Dim0SimplexKey(2)
        simplicial.Dim0SimplexKey(2)

    def test_create_dim_d_simplex_key(self):
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(2)
        simplicial.DimDSimplexKey(basis={v1, v2, v3})

    def test_generator_function(self):
        """test the simplex key generator"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(3)
        f = simplicial.DimDSimplexKey(basis={v1, v2, v3})
        assert simplicial.simplex_key({1, 2, 3}) == f
        assert simplicial.simplex_key(1) == v1
        assert simplicial.simplex_key(v1) == v1
        assert simplicial.simplex_key([1]) == v1
        assert simplicial.simplex_key({v1, v2, v3}) == f
        with pytest.raises(Exception):
            simplicial.simplex_key(1.124)
        with pytest.raises(Exception):
            simplicial.simplex_key("cats")

    def test_union(self):
        """test union"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(3)
        e = simplicial.DimDSimplexKey(basis={v1, v2})
        f = simplicial.DimDSimplexKey(basis={v1, v2, v3})
        assert v1 | v2 | v3 == f
        assert e | v3 == f
        assert v1 | v1 == v1

    def test_intersections(self):
        """test intersections"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(3)
        e = simplicial.DimDSimplexKey(basis={v1, v2})
        f = simplicial.DimDSimplexKey(basis={v1, v2, v3})
        assert f & v1 == v1
        assert e & f == e
        assert v1 & v1 == v1
        assert v1 & v2 == simplicial.DimDSimplexKey({})

    def test_difference(self):
        """test difference"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(3)
        e = simplicial.DimDSimplexKey(basis={v1, v2})
        f = simplicial.DimDSimplexKey(basis={v1, v2, v3})
        assert v1 - v1 == simplicial.DimDSimplexKey({})
        assert f - e == v3
        assert e - f == simplicial.DimDSimplexKey({})

    def test_iter(self):
        """test iter"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(3)
        e = simplicial.DimDSimplexKey(basis={v1, v2})
        f = simplicial.DimDSimplexKey(basis={v1, v2, v3})
        for b in f:
            assert b in f
        assert (e in f) is False

    def test_repr(self):
        """test repr"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(3)
        e = simplicial.DimDSimplexKey(basis={v1, v2})
        f = simplicial.DimDSimplexKey(basis={v1, v2, v3})
        str(e)  # these cant be tested against values because they can change order.
        str(f)
        assert str(v1) == "<1>"

    def test_equality(self):
        """test equality"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(1)
        v3 = simplicial.Dim0SimplexKey(3)
        assert v1 == v2
        assert v1 != v3
        assert v1 != "cat"

    def test_equivalence(self):
        """test union"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(1)
        assert v1 is not v2
        assert hash(v1) == hash(v2)  # Hashes are equivalent for 0-simplices

        v3 = simplicial.Dim0SimplexKey(3)
        # Assume you want to reference existing edge
        l1 = simplicial.simplex_key({v1, v3})
        l2 = simplicial.simplex_key({v1, v3})
        assert hash(l1) == hash(l1)
        assert l1 == l2
        assert hash(l1) == hash(l2)

    def test_compound_equality(self):
        """test compound equality"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        v3 = simplicial.Dim0SimplexKey(3)
        compound = simplicial.DimDSimplexKey(basis={v1, v2, v3})
        direct = simplicial.simplex_key({1, 2, 3})
        assert compound == direct

    def test_recursive_equality(self):
        """test recursive equality"""
        v1 = simplicial.Dim0SimplexKey(10)
        v2 = simplicial.Dim0SimplexKey(20)
        v3 = simplicial.Dim0SimplexKey(30)
        f = simplicial.DimDSimplexKey({v1, v2, v3})
        assert f.sub_keys == f.sub_keys


class TestMultiSimplices:
    """Test group for multi simplices"""

    def test_multi_edge_equivalence(self):
        """test multi edge"""
        v1 = simplicial.Dim0SimplexKey(1)
        v2 = simplicial.Dim0SimplexKey(2)
        l1 = simplicial.DimDSimplexKey({v1, v2}, multi=False)
        l2 = simplicial.DimDSimplexKey({v1, v2}, multi=True)
        assert l1 != l2

    def test_reference_multi(self):
        """test union"""
        v1 = simplicial.Dim0SimplexKey(3)
        v2 = simplicial.Dim0SimplexKey(4)
        l1 = simplicial.DimDSimplexKey({v1, v2}, multi=False)
        l2 = simplicial.DimDSimplexKey({v1, v2}, multi=True)

        # New reference to existing edge
        with pytest.raises(ValueError):
            l2_prime = simplicial.DimDSimplexKey({v1, v2})

        # Properly reference to existing edge
        l2_prime = simplicial.DimDSimplexKey({v1, v2}, multi=False, count_id=1)
        assert isinstance(l2_prime, simplicial.SimplexKey)

