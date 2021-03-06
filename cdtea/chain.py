"""
utilities for running chains on space_times
"""

from cdtea.metropolis import step
from cdtea.simplicial import Triangulation
import numpy as np
from cdtea.measurments import take_measurements




def run_chain(st: Triangulation, num_steps: int, measurements: list, sample_period: int, verbose: bool = False, lmbda=np.log(2)):
    """

    Args:
        num_steps: The number of steps to run the chain for
        sample_period: The number of steps between measurements.
        measurements: A list of functions that take in a triangulation and output a value to be added to a list
        st: The triangulation which will be chained. It is modified in place.
        verbose: if verbose each time a measurement is taken the percent completion is printed
    Returns: a list of measurement values for each measurement at each sampled point on the chain.

    """
    # this is where the measurements go
    samples = []

    # this keeps track of how many of each type of move succeeded.
    # success = np.zeros(3)


    try:
        for i in range(num_steps):
            if i % sample_period == 0:
                samples.append(take_measurements(st, measurements))

                if verbose:
                    print(100 * i / num_steps)
                    # print(success/i)
            step(st, lmbda=lmbda)



    # this is dangerous and bad. perhaps we should make a custom error class for expected failures (space_slice to small cant make a move)
    except Exception as e:
        print(e)
        print("nuggets")
        print(take_measurements(st, measurements))

    return samples
