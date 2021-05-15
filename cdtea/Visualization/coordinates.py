from cdtea.generate_flat import generate_flat_2d_space_time
from matplotlib import pyplot as plt
from cdtea import simplicial
from cdtea.simplicial import simplex_key
from collections import defaultdict

st = generate_flat_2d_space_time(space_size=10, time_size=10)
meta = st.simplex_meta


def get_t(face, meta):
    a = set()
    for b in face:
        a.add(meta[b]['t'])
    return tuple(a)


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


layers = defaultdict(list)
for tri in st.simplices[2]:
    layers[get_t(tri, meta)].append(tri)

#layers = {[tri for tri in st.simplices[2] if get_t(tri, meta)]}
print(layers)
