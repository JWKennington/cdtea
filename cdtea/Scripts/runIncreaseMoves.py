from cdtea import generate_flat
from cdtea import moves
from cdtea.Visualization.two_d_plot import two_d_plot
import numpy as np
from cdtea.tests.valid_triangulation import is_valid
import matplotlib.pyplot as plt
np.random.seed(1)
f = generate_flat.generate_flat_2d_space_time(time_size=8, space_size=8)

for _ in range(10):
    edge = np.random.choice(list(f.simplex_meta['s_type'].dual[(2, 0)]))
    print(edge)
    moves.add_2D(f, edge)
is_valid(f)
print('valid')
is_valid(f)
# print('valid')
two_d_plot(f)
plt.show()
