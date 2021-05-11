import cdtea.generate_flat
import cdtea.tests.valid_triangulation as validity
from cdtea.simplicial import DimDSimplexKey
st = cdtea.generate_flat.generate_flat_2d_space_time(23,23)
print(validity.edges_dont_cross_time_slices(st))
print(validity.is_valid(st))
