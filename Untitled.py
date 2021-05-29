import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from cdtea.util.TimeIndex import time_sep
from cdtea.generate_flat import generate_flat_2d_space_time

st = generate_flat_2d_space_time(10,10)


def get_future(st,tri):
    meta = st.simplex_meta
    for t in st.simplices[2]:
        overlap = t&tri
        if overlap.dim==1:
            if meta[overlap]["s_type"] == (2,0):
                pass

#print(np.random.mtrand.get_state())
G = nx.Graph()
meta = st.simplex_meta
for v in st.simplices[0]:
    G.add_node(v,t = meta[v]['t'])
for e in st.simplices[1]:
    if meta[e]["s_type"] == (1,1):
        basis = e.basis_list
        if not(meta[basis[0]]["t"]==0 and meta[basis[1]]["t"]==9):
            if not(meta[basis[0]]["t"]==9 and meta[basis[1]]["t"]==0):
                G.add_edge(*basis,color = 'b')

pos = nx.multipartite_layout(G, subset_key="t",align = "horizontal")


for e in st.simplices[1]:
    if meta[e]["s_type"] == (2,0):
        basis = e.basis_list
        if not(meta[basis[0]]["t"]==0 and meta[basis[1]]["t"]==4):
            if not(meta[basis[0]]["t"]==4 and meta[basis[1]]["t"]==0):
                G.add_edge(*basis,color = 'r')


#layers = [[v for v in st.simplices[0] if meta[v]["t"]==t] for t in range(st.time_size)]
#print(layers)
#pos = nx.shell_layout(G,nlist = layers)
#print(pos)
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]
pos = nx.spring_layout(G, pos = pos)
nx.draw(G,pos,with_labels = True,edge_color = colors)
plt.show()
