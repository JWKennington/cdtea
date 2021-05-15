from cdtea.generate_flat import generate_flat_2d_space_time
from matplotlib import pyplot as plt
from cdtea import simplicial
from cdtea.simplicial import simplex_key
from collections import defaultdict

st = generate_flat_2d_space_time(space_size=5, time_size=5)
meta = st.simplex_meta


def get_t(face):
    a = set()
    for b in face:
        a.add(meta[b]['t'])
    return tuple(sorted(list(a)))


def ordering(origin, layer):
    boundary = origin
    not_indexed = layer - {origin}
    index = {origin: 0}
    for i in range(len(layer)):
        for f in not_indexed:
            if (f & boundary).dim == 1:
                not_indexed -= {f}
                index[f] = index[boundary] + 1
                boundary = f
                break

    return index


def get_future(st: simplicial.Triangulation, face, layer):
    for f in st.simplices[2]:
        overlap = f & face
        if overlap.dim == 1:
            if meta[overlap]['s_type'] == (2, 0):
                if get_t(f) == tuple(sorted([(i + 1) % st.time_size for i in get_t(face)])):
                    return f
    right = get_right(face, layer)
    print(right)
    return get_future(st, right, layer)


def get_right(face, layer):
    order = ordering(face, layer)
    inv_map = {v: k for k, v in order.items()}
    return inv_map[1]


def alligned(l1, l2):
    l1_up = {}
    i = 0
    for t in l1:
        if meta[t]["s_type"] == (1, 2):
            l1_up[i] = t
            i += 1

    l2_down = {}
    i = 0
    for t in l2:
        if meta[t]["s_type"] == (2, 1):
            l2_down[i] = t
            i += 1
    val = True
    for i in range(len(l1_up)):
        t1 = l1_up[i]
        t2 = l2_down[i]
        val = val and (t1 & t2).dim == 1
    return val


def valid_complete_ordering(layers):
    T = len(layers)
    val = True
    for i in range(T):
        val = val and alligned(layers[i], layers[(i + 1) % T])
    return val




layers = defaultdict(set)
for tri in st.simplices[2]:
    layers[get_t(tri)].add(tri)

new_layers = []

for layer in layers:


ordering(list(layers[(0, 1)])[0], layers[(0, 1)])
orig = list(layers[(0, 1)])[1]
layer = layers[(0, 1)]
print(orig)
print(get_future(st, orig, layer))
print()
orig = list(layers[(0, 1)])[2]
layer = layers[(0, 1)]
print(orig)
print(get_future(st, orig, layer))
