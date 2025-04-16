
import numpy as np

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
        ia_time = (np.random.exponential(1 / self.lam)) * (np.random.uniform(self.a2l, self.a2u))
        self.time_passed += ia_time
        if (self.time_passed > self.time_end):
            self.time_passed = np.float64(0.00)
            raise StopIteration()
        
        return ia_time

a = RandomInterarrivalsIterator(
        np.float64(1.400), np.float64(0.600), np.float64(0.800), np.float64(10.00))
