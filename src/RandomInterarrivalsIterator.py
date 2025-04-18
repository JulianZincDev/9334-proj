
import numpy as np
from .rng import rng

class RandomInterarrivalsIterator:

    def __init__(self, lam: np.float64, a2l: np.float64, a2u: np.float64, time_end: np.float64):
        self.lam = lam
        self.a2l = a2l
        self.a2u = a2u
        self.time_end = time_end
        self.time_passed = np.float64(0.00)

    def __iter__(self):
        return self

    def __next__(self):
        # mean arrival rate = self.lam arrivals / minutes
        # mean interarrival time = 1 / (self.lam arrivals / minutes)
        #                        = minutes / (self.lam arrivals)
        #                        = (1 / self.lam) minutes per arrival
        #                        (average time for an arrival is (1 / self.lam) minutes)
        a1k = rng.exponential(1 / self.lam)
        # Then use numpy's exponential function to generate our first random number
        # exponential with mean = 1 / self.lam.

        # Then we have our bounds self.a2l, and self.a2u and we use numpy's uniform
        # method to generate a random number uniformly distributed in the provided interval
        a2k = rng.uniform(self.a2l, self.a2u)
        ia_time = a1k * a2k

        self.time_passed += ia_time
        if (self.time_passed > self.time_end):
            self.time_passed = np.float64(0.00)
            raise StopIteration()
        
        return ia_time
