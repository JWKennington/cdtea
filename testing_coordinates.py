from cdtea.Visualization.coordinates import toroidal_coordinates, nearest
from cdtea.generate_flat import generate_flat_2d_space_time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import LineCollection
from cdtea.Visualization.two_d_plot import two_d_plot
from cdtea.modifications import increase_move,decrease_move,parity_move
from cdtea.simplicial import simplex_key


ax = plt.gca()

st = generate_flat_2d_space_time(7, 9)
# meta = st.simplex_meta
# faces = st.simplices[2]
# f1 = list(faces)[20]
#
# for f in faces:
#     overlap = f & f1
#     if overlap in st.simplices[1]:
#         if meta[overlap]["s_type"] == (2, 0):
#             f2 = f
#             break
#
# increase_move(st, f1, f2)
# decrease_move(st, simplex_key(32*32))
# from random import choice
# for i in range(2):
#     f1 = choice(list(faces))
#     for f in faces:
#         overlap = f & f1
#         if overlap in st.simplices[1]:
#             if meta[overlap]["s_type"] == (1,1):
#                 f2 = f
#                 break
#
#     parity_move(st, f1, f2)

two_d_plot(st)
