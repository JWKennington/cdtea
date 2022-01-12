from cdtea import generate_flat
from cdtea import moves
from cdtea.Visualization.two_d_plot import two_d_plot
import numpy as np
from cdtea.tests.valid_triangulation import is_valid
import matplotlib.pyplot as plt

np.random.seed(1)

f = generate_flat.generate_flat_2d_space_time(time_size=8, space_size=8)

for _ in range(10):
	# TODO make simplex key sortable directly and remove str coercion
	edges = list(sorted(f.simplex_meta['s_type'].dual[(2, 0)], key=lambda x: str(x)))

	# edge = np.random.choice(edges)
	idx = np.random.randint(0, len(edges))
	edge = edges[idx]
	print('Add', idx, edge)
	moves.add_2D(f, edge)


for _ in range(10):
	# TODO make simplex key sortable directly and remove str coercion
	order_4_vertices = list(sorted(f.simplex_meta['order'].dual[4], key=lambda x: str(x)))

	# edge = np.random.choice(edges)
	idx = np.random.randint(0, len(order_4_vertices))
	vertex = order_4_vertices[idx]
	print('Remove', idx, vertex)
	moves.rem_2D(f, vertex)


is_valid(f)
print('valid')

# print('valid')

two_d_plot(f)

plt.show()
