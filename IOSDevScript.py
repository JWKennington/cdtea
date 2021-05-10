import cdtea.generate_flat
import cdtea.tests.valid_triangulation as validity
st = cdtea.generate_flat.generate_flat_2d_space_time(3,3)

print(validity.faces_imply_nodes(st))
