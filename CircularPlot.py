import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from cdtea.util.TimeIndex import time_sep
from cdtea.generate_flat import generate_flat_2d_space_time
from collections import defaultdict
from numpy import cos,sin,pi

from cdtea.modifications import increase_move
st = generate_flat_2d_space_time(4,6)
meta = st.simplex_meta
faces = st.simplices[2]
f1 = list(faces)[0]

for f in faces:
    overlap = f&f1
    if overlap in st.simplices[1]:
        if meta[overlap]["s_type"] == (2,0):
            f2 = f
            break
#increase_move(st,f1,f2)


#print(np.random.mtrand.get_state())
G = nx.Graph()
meta = st.simplex_meta

def get_pos(origin,layer):
    boundry = origin
    not_indexed = layer-{origin}
    index = {origin:0}
    for i in range(len(layer)):
        for f in not_indexed:
            if (f&boundry).dim == 1:
                
                not_indexed-={f}
                index[f] = index[boundry]+1
                boundry = f
                break
    return(index)
    

#construct the graph
for v in st.simplices[0]:
    boundry = []
    for e in st.simplices[1]:
        if v in e and meta[e]['s_type'] == (2,0):
            boundry.append(e-v)
    G.add_node(v,t = meta[v]['t'],boundryNondes = boundry)
for e in st.simplices[1]:
    if meta[e]["s_type"] == (1,1):
        basis = e.basis_list
        if not(meta[basis[0]]["t"]==0 and meta[basis[1]]["t"]==st.time_size-1):
            if not(meta[basis[0]]["t"]==st.time_size-1 and meta[basis[1]]["t"]==0):
                G.add_edge(*basis,color = 'b')
                pass
                
for e in st.simplices[1]:
    if meta[e]["s_type"] == (2,0):
        basis = e.basis_list
        #if not(meta[basis[0]]["t"]==0 and meta[basis[1]]["t"]==4):
            #if not(meta[basis[0]]["t"]==4 and meta[basis[1]]["t"]==0):
        G.add_edge(*basis,color = 'r')
                #pass

def to_cart(r,theta):
    #print(theta)
    return(np.array([r*cos(theta),r*sin(theta)]))
def to_pol(coords):
    return np.linalg.norm(coords),np.arctan2(coords[1],coords[0])

def get_pos(origin,layer):
    boundry = origin
    not_indexed = layer-{origin}
    index = {origin:0}
    for i in range(len(layer)):
        for f in not_indexed:
            if (f|boundry) in st.simplices[1]:
                
                not_indexed-={f}
                index[f] = index[boundry]+1
                boundry = f
                break
    return(index)
    
    
layers = {t:[v for v in st.simplices[0] if meta[v]["t"]==t] for t in range(st.time_size)}
positions = {t:get_pos(layers[t][0],set(layers[t])) for t in range(st.time_size)}
pos = {v:to_cart(meta[v]['t']+2,positions[meta[v]['t']][v]/len(layers[meta[v]['t']])*2*3.141) for v in st.simplices[0]}

def total_length(POS,layer1,layer2):
    total_length = 0
    i=0
    for e in st.simplices[1]:
        if any([l1 in e for l1 in layer1]) and any([l2 in e for l2 in layer2]):
            if meta[e]["s_type"] == (1,1):
                basis = e.basis_list
                if not(meta[basis[0]]["t"]==0 and meta[basis[1]]["t"]==st.time_size-1):
                    if not(meta[basis[0]]["t"]==st.time_size-1 and meta[basis[1]]["t"]==0):
                        edge = POS[basis[0]]-POS[basis[1]]
                        i+=1
                        total_length+=np.linalg.norm(edge)
    return total_length

offsets = [0,-3+25-.5,-4.5+25-.5,10+.5,5]
offsets = [0,21.5,20,10.5,5]
offsets = [0,0,0,0,0]
#offsets = [0,21,19,9,6987]
test_offsets = []
orig_offset = 0
temp_pos = pos   

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]


for t in layers:
    current_length = total_length(temp_pos,layers[t],layers[(t-1)%st.time_size])
    
    
        
    for offset in range(1,2*len(layers[t])-1):
        offset = offset/2.
        if t == 0:
            final_offset = 0
            break
        orig_offset = offset
        offset = offset/len(layers[t])*2*pi
        new_pos = {}
        for v in st.simplices[0]:
            if v in layers[t]:
                new_pos[v] = to_cart(t+1,offset+positions[t][v]/len(layers[t])*2*3.141)
            else:
                new_pos[v] = temp_pos[v]
        
        new_length = total_length(new_pos,layers[t],layers[(t-1)%st.time_size])
        
        
        new_pos2 = new_pos
        for v in layers[t]:
            new_pos2[v] = to_cart(t+1,offset-positions[t][v]/len(layers[t])*2*3.141)
        
        if total_length(new_pos2,layers[t],layers[(t-1)%st.time_size])<new_length:
            new_pos = new_pos2
            offsets[t] = -orig_offset
            final_offset = -orig_offset
            new_length = total_length(new_pos2,layers[t],layers[(t-1)%st.time_size])
            print("Glabella")
        
        
        print(t,orig_offset,new_length,current_length)
        if new_length < current_length:
            offsets[t] = orig_offset
            final_offset = orig_offset
            current_length = new_length
            temp_pos = new_pos
        
    print("For layer {t} the offset is {offset}".format(t=t,offset = final_offset))
    print()
    
    
    
    plt.figure(figsize=(18,18))
    nx.draw(G,temp_pos,with_labels = False,edge_color = colors,node_size = 50)

    plt.show()
    plt.close()


offsets = [0,-3+25-.5,-4.5+25-.5,10+.5,5]
for t in layers:
        l = len(layers[t])
        for v in layers[t]:
            offset = offsets[t]
            r,theta = to_pol(temp_pos[v])
            if offset<0:
                theta = -theta
            offset = abs(offset)
            theta+=offset/l*2*pi
            temp_pos[v] = to_cart(r,theta)
  
plt.figure(figsize=(18,18))
nx.draw(G,temp_pos,with_labels = False,edge_color = colors,node_size = 50)

plt.show()
plt.close()
