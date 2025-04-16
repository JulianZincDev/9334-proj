import numpy as np
from numpy.typing import NDArray
from .RandomInterarrivalsIterator import RandomInterarrivalsIterator
from .RandomServiceTimesIterator import RandomServiceTimesIterator
from .sim import sim

def random_sim(n: int, h: int, time_end: np.float64, lam: np.float64, a2l: np.float64, a2u: np.float64, ps: NDArray[np.float64], mu, alph):
    # TODO: make an iterable that just continually randomly generates the
    # interarrival times based on the two above random numbers

    interarrival_times = RandomInterarrivalsIterator(lam, a2l, a2u, time_end)
    service_times = RandomServiceTimesIterator(mu, alph, ps)
    return sim(n, h, interarrival_times, service_times)
    



            

