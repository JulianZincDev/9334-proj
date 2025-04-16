
import numpy as np
from numpy.typing import NDArray

class RandomServiceTimesIterator:

    def __init__(self, mu: np.float64, alph: np.float64, ps: NDArray[np.float64]):
        self.mu = mu
        self.alph = alph
        self.ps = ps

    def find_num_sub_jobs(self):
        lower_prob_bounds = 0.00
        higher_prob_bounds = 0.00

        job_number_randomizer = np.random.uniform(0, 1)
        # print(job_number_randomizer)
        # print(ps)
        num_sub_jobs = 1

        for index, p in enumerate(self.ps, 1):
            lower_prob_bounds = higher_prob_bounds
            higher_prob_bounds += p
            if job_number_randomizer >= lower_prob_bounds and job_number_randomizer < higher_prob_bounds:
                num_sub_jobs = index
            

        return num_sub_jobs


    def __iter__(self):
        return self


    # https://webcms3.cse.unsw.edu.au/static/uploads/course/COMP9334/25T1/58d47d8ec72353ed869643ef34445a7b935a5a4598d21316862901c822ad958f/week05B_2.pdf
    # As the above Week5B lecture notes explain, we used the inverse transform to come up
    # with the formula to use for randomization in the distribution with the given CDF
    def inverse_transformed_CDF(self, u):
        return ((-np.log(1 - u))**(1/self.alph)) / self.mu
        

    def __next__(self):
        service_times = []
        for i in range(self.find_num_sub_jobs()):
            service_times.append(self.inverse_transformed_CDF(np.random.uniform(0, 1)))
        return service_times

a = RandomServiceTimesIterator(
    np.float64(1.100), np.float64(1.210), np.array([np.float64(0.400), np.float64(0.300),
                                                    np.float64(0.200), np.float64(0.050),
                                                    np.float64(0.050)]))
