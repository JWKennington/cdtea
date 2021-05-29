import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from cdtea.util.TimeIndex import time_sep
from cdtea.generate_flat import generate_flat_2d_space_time
from collections import defaultdict
from numpy import cos,sin,pi

from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.Visualization.SpatialOrdering import spatial_ordering
from cdtea.simplicial import simplex_key
from copy import deepcopy



from cdtea.modifications import increase_move,parity_move,decrease_move

st = generate_flat_2d_space_time(5,10)
meta = st.simplex_meta
T = st.time_size
G = nx.Graph()

faces = st.simplices[2]
f1 = list(faces)[20]


for f in faces:
    overlap = f&f1
    if overlap in st.simplices[1]:
        if meta[overlap]["s_type"] == (2,0):
            f2 = f
            break
            
            
increase_move(st,f1,f2)
decrease_move(st,simplex_key(50))





def plot(p1):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_aspect(aspect=1)
    
    fixed_nodes = []
    for prev_t in range(t+2):
        for v in layers[prev_t]:
            fixed_nodes.append(v)
    sub_G = G.subgraph(fixed_nodes)
    
    
    nx.draw(sub_G,p1,with_labels = False,node_size = 0)
    #ax2 = fig.add_subplot(122)
    #ax2.set_aspect(aspect = 1)
    #nx.draw(sub_G,p2,with_labels = False,node_size = 0)
    
    plt.show()
    plt.close()



#construct the graph
for v in st.simplices[0]:
    G.add_node(v,t = meta[v]['t'])
for e in st.simplices[1]:
    if meta[e]["s_type"] == (1,1):
        basis = e.basis_list
        t0,t1 = meta[basis[0]]["t"],meta[basis[1]]["t"]
        if not(t0==0 and t1==T-1) and not(t0==T-1 and t1==0):
            G.add_edge(*basis,color = 'b')
            pass
    if meta[e]["s_type"] == (2,0):
        basis = e.basis_list
        G.add_edge(*basis,color = 'r')
colors = [G[u][v]['color'] for u,v in G.edges()]
        
def to_cart(r:float,theta:float):
    return(np.array([r*cos(theta),r*sin(theta)]))
def to_pol(coords:list):
    return np.linalg.norm(coords),np.arctan2(coords[1],coords[0])
    
def layer_length(POS,layer1,layer2):
    total_length = 0
    
    #loop over all edges
    for e in st.simplices[1]:
        #only count those edges that have a vertex in each layer
        if any([l1 in e for l1 in layer1]) and any([l2 in e for l2 in layer2]):
            basis = e.basis_list
            t0,t1 = meta[basis[0]]["t"],meta[basis[1]]["t"]
            if not(t0==0 and t1==T-1) and not(t0==T-1 and t1==0):
                edge = POS[basis[0]]-POS[basis[1]]                        
                total_length+=np.linalg.norm(edge)
    return total_length
    
    
layers = {t:[v for v in st.simplices[0] if meta[v]["t"]==t] for t in range(st.time_size)}
positions = {t:spatial_ordering(st,layers[t]) for t in range(st.time_size)}

#set up the initial position
pol_pos = {v:[2*meta[v]['t']+T/2,positions[meta[v]['t']][v]/len(layers[meta[v]['t']])*2*pi] for v in st.simplices[0]}

pos = {v:to_cart(pol_pos[v][0],pol_pos[v][1]) for v in st.simplices[0]}




#for each time slice
for t in range(T-1):
    print(t)
    #print("===================")
    #print("layer {}".format(t))
    layer1 = layers[t]
    L1 = len(layer1)
    layer2 = layers[t+1] #this should never fail becouse of the max t is T-1
    L2 = len(layer2)
    
    current_lenth = layer_length(pos,layers[t],layers[(t+1)%T])
    temp_pol_pos = deepcopy(pol_pos)
    temp_pos = deepcopy(pos)
    
    
    delta_theta = 1/(2.0*L1)*2*pi
    
    
    
    
    
    #check all rotational orientations and choose the one that minimizes that layers total edge length
    for direction in [1,-1]:
        #print(" Direction {}".format(direction))
        
        for iteration in range(2*L1):
            
            
            #plot()
            
            #print(iteration)
            if True:
                for prev_t in range(t+1):
                
                    
                    #print(prev_t)
                    for v in layers[prev_t]:
                        temp_pol_pos[v][1]+=delta_theta
            
                if direction == -1 and iteration == 0:
                    for v in layers[t+1]:
                        temp_pol_pos[v][1]*=-1
            
            temp_pos = {v:to_cart(temp_pol_pos[v][0],temp_pol_pos[v][1]) for v in st.simplices[0]}
            
        
            #plot()
            
            
                
            temp_length = layer_length(temp_pos,layers[t],layers[(t+1)])
            
            
            
            
                
                
            
            
            if temp_length<current_lenth:
                #print("New best angle, updating.")
                #print(temp_length)
                current_lenth = temp_length
                #plot()
                pol_pos = deepcopy(temp_pol_pos)
                
                pos = deepcopy(temp_pos)
                
            
    #test_pos = {v:to_cart(pol_pos[v][0],pol_pos[v][1]) for v in st.simplices[0]}
    #plot(pos)
            
                
                
                
        


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect(aspect=1)
nx.draw(G,pos,with_labels = False,edge_color = colors,node_size = 5)
plt.show()
plt.close()

