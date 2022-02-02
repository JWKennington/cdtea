"""Tests for the simplicial module"""

from cdtea import simplicial, moves


class TestMoves2D:
    """Tests for the 2-Dimensional Moves"""

    def test_add_2d(self):
        """Test 2d add"""

        ################################################################################
        #               CREATE TRIANGULATION - TODO SIMPLIFY WITH UTILITIES            #
        ################################################################################
        trg = simplicial.Triangulation(time_size=None)

        # Vertices
        vertices = [simplicial.Dim0SimplexKey(key=i) for i in range(4)]
        v0, v1, v2, v3 = vertices
        v_time_idx = [0, 1, 1, 2]

        # Edges
        edges = [
            simplicial.DimDSimplexKey({v0, v1}),
            simplicial.DimDSimplexKey({v0, v2}),
            simplicial.DimDSimplexKey({v1, v2}),
            simplicial.DimDSimplexKey({v1, v3}),
            simplicial.DimDSimplexKey({v2, v3}),
        ]
        edge_types = 2 * [(1, 1)] + [(2, 0)] + 2 * [(1, 1)]

        # Faces
        faces = [
            simplicial.DimDSimplexKey({v0, v1, v2}),
            simplicial.DimDSimplexKey({v1, v2, v3}),
        ]
        face_types = [(1, 2), (2, 1)]

        # Add simplices to triangulation
        for v, t in zip(vertices, v_time_idx):
            trg.add_simplex(v, t=t, order=0)

        for e, s_type in zip(edges, edge_types):
            trg.add_simplex(e, s_type=s_type)
            for v in e.basis:
                trg.simplex_meta['order'][v] += 1

        for f, s_type in zip(faces, face_types):
            trg.add_simplex(f, s_type=s_type)

        ################################################################################
        #                               Perform move                                   #
        ################################################################################

        moves.add_2d(trg, edge=edges[2])

        ################################################################################
        #              COMPARE TRIANGULATION - TODO SIMPLIFY WITH UTILITIES            #
        ################################################################################

        trg_exp = simplicial.Triangulation(time_size=None)

        # Vertices
        vertices = [simplicial.Dim0SimplexKey(key=i) for i in range(5)]
        v0, v1, v2, v3, v4 = vertices
        v_time_idx = [0, 1, 1, 2, 1]

        # Edges
        edges = [
            simplicial.DimDSimplexKey({v0, v1}),
            simplicial.DimDSimplexKey({v0, v2}),
            simplicial.DimDSimplexKey({v1, v4}),
            simplicial.DimDSimplexKey({v4, v2}),
            simplicial.DimDSimplexKey({v1, v3}),
            simplicial.DimDSimplexKey({v2, v3}),
            simplicial.DimDSimplexKey({v0, v4}),
            simplicial.DimDSimplexKey({v3, v4}),
        ]
        edge_types = 2 * [(1, 1)] + 2 * [(2, 0)] + 4 * [(1, 1)]

        # Faces
        faces = [
            simplicial.DimDSimplexKey({v0, v1, v4}),
            simplicial.DimDSimplexKey({v0, v2, v4}),
            simplicial.DimDSimplexKey({v1, v3, v4}),
            simplicial.DimDSimplexKey({v2, v3, v4}),
        ]
        face_types = [(1, 2), (1, 2), (2, 1), (2, 1)]

        # Add simplices to triangulation
        for v, t in zip(vertices, v_time_idx):
            trg_exp.add_simplex(v, t=t, order=0)

        for e, s_type in zip(edges, edge_types):
            trg_exp.add_simplex(e, s_type=s_type)
            for v in e.basis:
                trg_exp.simplex_meta['order'][v] += 1

        for f, s_type in zip(faces, face_types):
            trg_exp.add_simplex(f, s_type=s_type)

        assert trg == trg_exp

    def test_rem_2d(self):
        """Test 2d remove"""

        ################################################################################
        #               CREATE TRIANGULATION - TODO SIMPLIFY WITH UTILITIES            #
        ################################################################################

        trg = simplicial.Triangulation(time_size=None)

        # Vertices
        vertices = [simplicial.Dim0SimplexKey(key=i) for i in range(5)]
        v0, v1, v2, v3, v4 = vertices
        v_time_idx = [0, 1, 1, 2, 1]

        # Edges
        edges = [
            simplicial.DimDSimplexKey({v0, v1}),
            simplicial.DimDSimplexKey({v0, v2}),
            simplicial.DimDSimplexKey({v1, v4}),
            simplicial.DimDSimplexKey({v4, v2}),
            simplicial.DimDSimplexKey({v1, v3}),
            simplicial.DimDSimplexKey({v2, v3}),
            simplicial.DimDSimplexKey({v0, v4}),
            simplicial.DimDSimplexKey({v3, v4}),
        ]
        edge_types = 2 * [(1, 1)] + 2 * [(2, 0)] + 4 * [(1, 1)]

        # Faces
        faces = [
            simplicial.DimDSimplexKey({v0, v1, v4}),
            simplicial.DimDSimplexKey({v0, v2, v4}),
            simplicial.DimDSimplexKey({v1, v3, v4}),
            simplicial.DimDSimplexKey({v2, v3, v4}),
        ]
        face_types = [(1, 2), (1, 2), (2, 1), (2, 1)]

        # Add simplices to triangulation
        for v, t in zip(vertices, v_time_idx):
            trg.add_simplex(v, t=t, order=0)

        for e, s_type in zip(edges, edge_types):
            trg.add_simplex(e, s_type=s_type)
            for v in e.basis:
                trg.simplex_meta['order'][v] += 1

        for f, s_type in zip(faces, face_types):
            trg.add_simplex(f, s_type=s_type)

        ################################################################################
        #                               Perform move                                   #
        ################################################################################

        moves.rem_2d(trg, node=v4)

        ################################################################################
        #              COMPARE TRIANGULATION - TODO SIMPLIFY WITH UTILITIES            #
        ################################################################################
        trg_exp = simplicial.Triangulation(time_size=None)

        # Vertices
        vertices = [simplicial.Dim0SimplexKey(key=i) for i in range(4)]
        v0, v1, v2, v3 = vertices
        v_time_idx = [0, 1, 1, 2]

        # Edges
        edges = [
            simplicial.DimDSimplexKey({v0, v1}),
            simplicial.DimDSimplexKey({v0, v2}),
            simplicial.DimDSimplexKey({v1, v2}),
            simplicial.DimDSimplexKey({v1, v3}),
            simplicial.DimDSimplexKey({v2, v3}),
        ]
        edge_types = 2 * [(1, 1)] + [(2, 0)] + 2 * [(1, 1)]

        # Faces
        faces = [
            simplicial.DimDSimplexKey({v0, v1, v2}),
            simplicial.DimDSimplexKey({v1, v2, v3}),
        ]
        face_types = [(1, 2), (2, 1)]

        # Add simplices to triangulation
        for v, t in zip(vertices, v_time_idx):
            trg_exp.add_simplex(v, t=t, order=0)

        for e, s_type in zip(edges, edge_types):
            trg_exp.add_simplex(e, s_type=s_type)
            for v in e.basis:
                trg_exp.simplex_meta['order'][v] += 1

        for f, s_type in zip(faces, face_types):
            trg_exp.add_simplex(f, s_type=s_type)

        assert trg == trg_exp

    def test_parity_2d(self):
        """Test 2d parity"""

        ################################################################################
        #               CREATE TRIANGULATION - TODO SIMPLIFY WITH UTILITIES            #
        ################################################################################
        trg = simplicial.Triangulation(time_size=None)  # None time size for cylindrical topology

        # Vertices
        vertices = [simplicial.Dim0SimplexKey(key=i) for i in range(4)]
        v0, v1, v2, v3 = vertices
        v_time_idx = [0, 0, 1, 1]

        # Edges
        edges = [
            simplicial.DimDSimplexKey({v0, v1}),
            simplicial.DimDSimplexKey({v2, v3}),

            simplicial.DimDSimplexKey({v0, v2}),
            simplicial.DimDSimplexKey({v1, v3}),

            simplicial.DimDSimplexKey({v1, v2}),
        ]
        edge_types = 2 * [(2, 0)] + 3 * [(1, 1)]

        # Faces
        faces = [
            simplicial.DimDSimplexKey({v0, v1, v2}),
            simplicial.DimDSimplexKey({v1, v2, v3}),
        ]
        face_types = [(2, 1), (1, 2)]

        # Add simplices to triangulation
        for v, t in zip(vertices, v_time_idx):
            trg.add_simplex(v, t=t, order=0)

        for e, s_type in zip(edges, edge_types):
            trg.add_simplex(e, s_type=s_type)
            for v in e.basis:
                trg.simplex_meta['order'][v] += 1

        for f, s_type in zip(faces, face_types):
            trg.add_simplex(f, s_type=s_type)

        ################################################################################
        #                               Perform move                                   #
        ################################################################################

        moves.parity_2d(trg, edge=edges[-1])

        ################################################################################
        #              COMPARE TRIANGULATION - TODO SIMPLIFY WITH UTILITIES            #
        ################################################################################
        trg_exp = simplicial.Triangulation(time_size=None)  # None time size for cylindrical topology

        # Vertices
        vertices = [simplicial.Dim0SimplexKey(key=i) for i in range(4)]
        v0, v1, v2, v3 = vertices
        v_time_idx = [0, 0, 1, 1]

        # Edges
        edges = [
            simplicial.DimDSimplexKey({v0, v1}),
            simplicial.DimDSimplexKey({v2, v3}),

            simplicial.DimDSimplexKey({v0, v2}),
            simplicial.DimDSimplexKey({v1, v3}),
            simplicial.DimDSimplexKey({v0, v3}),
        ]
        edge_types = 2 * [(2, 0)] + 3 * [(1, 1)]

        # Faces
        faces = [
            simplicial.DimDSimplexKey({v0, v1, v3}),
            simplicial.DimDSimplexKey({v0, v2, v3}),
        ]
        face_types = [(2, 1), (1, 2)]

        # Add simplices to triangulation
        for v, t in zip(vertices, v_time_idx):
            trg_exp.add_simplex(v, t=t, order=0)

        for e, s_type in zip(edges, edge_types):
            trg_exp.add_simplex(e, s_type=s_type)
            for v in e.basis:
                trg_exp.simplex_meta['order'][v] += 1

        for f, s_type in zip(faces, face_types):
            trg_exp.add_simplex(f, s_type=s_type)

        assert trg == trg_exp
