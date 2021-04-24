from cdtea import simplicial
from cdtea import generate_flat


class TestGenerateFlat:

    def test_create(self):
        """This test makes sure that generate_flat creates a triangulation
        """
        t = generate_flat.generate_flat_2d_space_time(3, 3)

        assert isinstance(t, simplicial.Triangulation)


    # additional test ideas. Waiting to implement these until more tools for accessing simplex data have been constructed.
    # each vertex has 6 adjacent edges
    # each vertex has 6 adjacent triangles
    # each vertex has two space-like edges
    # each vertex has 4 time like edges (two past pointing and two future pointing)
    # test total vertex/edge/triangle count
