from cdtea import generate_flat
from cdtea import moves
from cdtea.Visualization.two_d_plot import two_d_plot
import numpy as np
import matplotlib.pyplot as plt

plt.interactive(True)
import matplotlib

matplotlib.use('TkAgg')


# np.random.seed(1)


def is_mixed_face_edge(edge, trg):
    faces = trg.contains(edge, dim=2)
    face_types = set([trg.simplex_meta['s_type'][f] for f in faces])
    return len(face_types) == 2


trg = generate_flat.generate_flat_2d_space_time(time_size=32, space_size=32)
#
for _ in range(1000):
    # TODO make simplex key sortable directly and remove str coercion
    edges = list(sorted(trg.simplex_meta['s_type'].dual[(2, 0)], key=lambda x: str(x)))

    # edge = np.random.choice(edges)
    idx = np.random.randint(0, len(edges))
    edge = edges[idx]
    print('Add', idx, edge)
    moves.add_2D(trg, edge)

for _ in range(500):
    # TODO make simplex key sortable directly and remove str coercion
    order_4_vertices = list(sorted(trg.simplex_meta['order'].dual[4], key=lambda x: str(x)))

    # edge = np.random.choice(edges)
    idx = np.random.randint(0, len(order_4_vertices))
    vertex = order_4_vertices[idx]
    print('Remove', idx, vertex)
    moves.rem_2D(trg, vertex)


for _ in range(500):
    # TODO make simplex key sortable directly and remove str coercion
    edges = list(sorted(trg.simplex_meta['s_type'].dual[(1, 1)], key=lambda x: str(x)))

    mixed_face_edges = [e for e in edges if is_mixed_face_edge(e, trg)]

    # edge = np.random.choice(edges)
    idx = np.random.randint(0, len(mixed_face_edges))
    edge = mixed_face_edges[idx]
    print('Parity', idx, edge)
    moves.parity_2D(trg, edge)






# print('validating')
# is_valid(trg)
# print('valid')


two_d_plot(trg)
plt.show()
plt.pause(1000000)
# plt.pause(np.infty)
