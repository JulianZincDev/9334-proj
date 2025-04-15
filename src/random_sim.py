import numpy as np
from numpy.typing import NDArray


def random_sim(lam: np.float64, a2l: np.float64, a2u: np.float64, ps: NDArray[np.float64], mu, alph):
    print(f'exp rand: {np.random.exponential(1 / lam)}')
    print(f'uniform rand: {np.random.uniform(a2l, a2u)}')
    # TODO: make an iterable that just continually randomly generates the
    # interarrival times based on the two above random numbers


    def find_num_sub_jobs():
        lower_prob_bounds = 0.00
        higher_prob_bounds = 0.00

        job_number_randomizer = np.random.uniform(0, 1)
        print(job_number_randomizer)
        print(ps)
        num_sub_jobs = 1

        for index, p in enumerate(ps, 1):
            lower_prob_bounds = higher_prob_bounds
            higher_prob_bounds += p
            if job_number_randomizer >= lower_prob_bounds and job_number_randomizer < higher_prob_bounds:
                num_sub_jobs = index
            

        return num_sub_jobs

    print(find_num_sub_jobs())
    

            

