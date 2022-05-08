from cdtea import chain
from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.Visualization import two_d_plot
import matplotlib.pyplot as plt
import numpy as np
import cdtea.measurments as mes
import cdtea.simplicial as simplicial

# results = []
# mi,ma = .1,1
# lambdas = np.linspace(mi, ma, 10)
# for l in lambdas:
#     st = generate_flat_2d_space_time(space_size=8, time_size=8)
#     result = chain.run_chain(st, 10000, [mes.average_length], 999, verbose=True)[-1][0]
#     results.append(result/8.)
# x = np.linspace(mi, ma, 1000)
# plt.plot(x, 1 / np.sqrt(2 * x))
# plt.plot(lambdas, results, 'o')
# plt.show()

st = generate_flat_2d_space_time(space_size=8, time_size=8)


def action_without_matter(st: simplicial.Triangulation):
    N = 0
    for n in st.nodes:
        N += 1
    return -np.log(2) * N


def einstein_hilbert(st: simplicial.Triangulation):
    order = st.simplex_meta['order']
    tot = 0
    Lambda = 0
    ae = 1
    for n in st.nodes:
        # the deficit angle
        epsilon = 2 * np.pi / 6 * (order[n] - 6)

        tot += 1 / (8 * np.pi) * ae * (epsilon / ae - Lambda)
    print(f"The total is {tot}")
    return -np.log(2) * st.num_nodes


def dilaton(st: simplicial.Triangulation):
    order = st.simplex_meta['order']
    phi = st.simplex_meta['dilaton']
    contains = st.simplex_meta['contains'].dual
    tot = 0
    Lambda = 0
    ae = 1

    def w(p):
        return p

    for f in st.faces:
        # the average deficit angle
        epsilon = 0
        for n in f:
            Tri_Number = simplicial.filter_simplices(contains[n], dim=2)

            # The effective "deficit angle" for each face
            # each node contributes angle inversely proportianal to the number of triangles its a part of
            epsilon += (2 * np.pi / 6 * (order[n] - 6)) / len(Tri_Number)
        epsilon = epsilon / 3
        R = epsilon / ae

        edges = simplicial.filter_simplices(st.simplex_meta['contains'][f], dim=1)
        for edge in edges:
            nodes = edge.basis_list
            t = st.simplex_meta['t']
            if t[nodes[0]] == t[nodes[1]]:
                spatial_edge = edge
                break

        temporal_face = contains[spatial_edge]-{f,}
        temporal_phi = phi[temporal_face.pop()]
        d_phi_t = temporal_phi-phi[f]
        """
        There is a serious derivative problem here unless we define a global left and right parity.
        without that the direction of a derivative isnt clear. 
        """
        d_phi_x = 0

        tot += 1 / (8 * np.pi) * ae * (phi[f] * R - w(phi[f]) / phi[f] - Lambda)
    print(f"The total is {tot}")
    return -np.log(2) * st.num_nodes


# def dilaton_action(st: simplicial.Triangulation):
# total_action = 0.
#
# def v(phi):
#     return phi
# k = 1
# phi = st.simplex_meta["dilaton"]
# for n in st.faces:
#     Delta_t_phi =
#     delta_x_phi =
#     (1/(2*k)*(phi*R-w(phi[n])/phi[n]*))
#     total_action += v(phi)
# return -np.log(2) * st.num_nodes


# chain.run_chain(st, action, 1000, [], 1000, verbose=True)
st, data = chain.run_chain(st, dilaton, 10000, [mes.volume_profile], 10, verbose=True)
data = np.array(data).flatten()
plt.hist(data)
plt.show()
two_d_plot.two_d_plot(st)
plt.show()
