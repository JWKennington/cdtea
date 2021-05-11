import cdtea.generate_flat
import cdtea.tests.valid_triangulation as validity
from cdtea.simplicial import DimDSimplexKey
st = cdtea.generate_flat.generate_flat_2d_space_time(3,3)
print(validity.is_valid(st))
