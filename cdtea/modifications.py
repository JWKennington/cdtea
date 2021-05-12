from cdtea.simplicial import Triangulation, SimplexKey, DimDSimplexKey, Dim0SimplexKey, simplex_key
from cdtea.generate_flat import generate_flat_2d_space_time as gen

tri = gen(space_size=5, time_size=5)


def parity_move(triangulation: Triangulation, k1: SimplexKey, k2: SimplexKey):
    overlap = k1 & k2
    if overlap in triangulation.simplices[1]:
        s_type = triangulation.simplex_meta[overlap]["s_type"]
        if s_type == (1, 1):
            pass
        else:
            raise Exception("Faces are temporal neighbors not spatial neighbors")
    else:
        raise Exception("Faces are not neighbors")


key1 = simplex_key({1, 21, 22})
key2 = simplex_key({1, 2, 22})
parity_move(tri, key1, key2)
