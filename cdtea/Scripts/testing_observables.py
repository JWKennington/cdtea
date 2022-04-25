from cdtea import chain
from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.Visualization import two_d_plot
import matplotlib.pyplot as plt
import numpy as np
import cdtea.measurments as mes

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
chain.run_chain(st, 10000, [], 10000, verbose=False)
data = chain.run_chain(st, 100000, [mes.volume_profile], 1000, verbose=True)
data = np.array(data).flatten()
plt.hist(data)
plt.show()
