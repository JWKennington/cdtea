from cdtea import generate_flat
from cdtea import moves, simplicial
from cdtea.Visualization.two_d_plot import two_d_plot
import numpy as np
from cdtea.tests.valid_triangulation import is_valid
import matplotlib.pyplot as plt

np.random.seed(1)


def is_mixed_face_edge(edge, trg):
    faces = trg.contains(edge, dim=2)
    face_types = set([trg.simplex_meta['s_type'][f] for f in faces])
    return len(face_types) == 2


trg = generate_flat.generate_flat_2d_space_time(time_size=8, space_size=8)

for _ in range(10):
    # TODO make simplex key sortable directly and remove str coercion
    edges = list(sorted(trg.simplex_meta['s_type'].dual[(2, 0)], key=lambda x: str(x)))

    # edge = np.random.choice(edges)
    idx = np.random.randint(0, len(edges))
    edge = edges[idx]
    print('Add', idx, edge)
    moves.add_2d(trg, edge)

for _ in range(10):
    # TODO make simplex key sortable directly and remove str coercion
    order_4_vertices = list(sorted(trg.simplex_meta['order'].dual[4], key=lambda x: str(x)))

    # edge = np.random.choice(edges)
    idx = np.random.randint(0, len(order_4_vertices))
    vertex = order_4_vertices[idx]
    print('Remove', idx, vertex)
    moves.rem_2d(trg, vertex)

for _ in range(10):
    # TODO make simplex key sortable directly and remove str coercion
    edges = list(sorted(trg.simplex_meta['s_type'].dual[(1, 1)], key=lambda x: str(x)))

    mixed_face_edges = [e for e in edges if is_mixed_face_edge(e, trg)]

    # edge = np.random.choice(edges)
    idx = np.random.randint(0, len(mixed_face_edges))
    edge = mixed_face_edges[idx]
    print('Parity', idx, edge)
    moves.parity_2d(trg, edge)

is_valid(trg)
print('valid')

# print('valid')

# two_d_plot(trg)

plt.show()
