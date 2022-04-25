from cdtea.generate_flat import generate_flat_2d_space_time
from cdtea.chain import run_chain
from cdtea.measurments import volume_profile, volume
import matplotlib.pyplot as plt
import numpy as np

all_data = []
st = generate_flat_2d_space_time(space_size=16, time_size=16)

num_steps = 1000
sample_period = 1

lmbda_max = .2
num_lmbda_samples = 6
lmbdas = np.linspace(0, lmbda_max, num_lmbda_samples)

# x = np.arange(0, num_steps, 10)
datas = []
for l in lmbdas:
    print(l)
    start = generate_flat_2d_space_time(space_size=16, time_size=16)
    chain = run_chain(start, num_steps, [volume], sample_period, verbose=False, lmbda=l)
    datas.append(chain)

for i, data in enumerate(datas):
    plt.plot(data, label=f"λ = {lmbdas[i]}")

plt.title("16x16 flat st, change in volume over 1000 iterations")
plt.legend()
plt.show()
