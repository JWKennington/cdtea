from cdtea.simplicial import Triangulation, SimplexKey, DimDSimplexKey, Dim0SimplexKey, simplex_key
from cdtea.generate_flat import generate_flat_2d_space_time as gen
from cdtea.tests import valid_triangulation as validity

tri = gen(space_size=5, time_size=5)


def parity_move(triangulation: Triangulation, k1: SimplexKey, k2: SimplexKey):
    overlap = k1 & k2
    union = k1 | k2
    non_overlap = union - overlap
    # print(union)
    if overlap in triangulation.simplices[1]:
        s_type = triangulation.simplex_meta[overlap]["s_type"]
        if s_type == (1, 1):
            # This is where we modify the triangulation
            # The dim 0 simplices remain unchanged.

            # the dim 1 simplices. the spatial edge is removed and replaced with another
            triangulation.remove_simplex(overlap)
            triangulation.add_simplex(non_overlap, s_type=(1, 1))

            # the dim 2 simplices, the two associated with the overlap are removed and the two new ones added
            triangulation.remove_simplex(k1)
            triangulation.remove_simplex(k2)
            overlap_list = overlap.basis_list
            times = [triangulation.simplex_meta[b]['t'] for b in overlap_list]
            overlap_list = [x for _, x in sorted(zip(times, overlap_list))]
            triangulation.add_simplex(non_overlap | overlap_list[0], s_type=(1, 2))
            triangulation.add_simplex(non_overlap | overlap_list[1], s_type=(2, 1))

            pass
        else:
            raise Exception("Faces are temporal neighbors not spatial neighbors")
    else:
        raise Exception("Faces are not neighbors")


key1 = simplex_key({1, 21, 22})
key2 = simplex_key({1, 2, 22})
parity_move(tri, key1, key2)
validity.is_valid(tri)
