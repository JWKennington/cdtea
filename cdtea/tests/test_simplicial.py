"""Tests for the simplicial module"""

from cdtea import simplicial


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
        t.add_simplex(e34, edge_type='spatial')
        t.add_simplex(e31, edge_type='temporal')
        t.add_simplex(e42, edge_type='temporal')

        t.add_simplex(f1, dilaton=0.5)
        t.add_simplex(f2, dilaton=0.6)

        assert isinstance(t, simplicial.Triangulation)
