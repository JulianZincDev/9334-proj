from numpy.typing import NDArray
from typing import Iterable
import numpy as np
import io


def format_output(mrt: float, finished_jobs: list[tuple[float, float]]):
    mrt_string = f'{mrt:.4f}\n'

    dep_string = '\n'.join([f'{arrival_time:.4f}   {departure_time:.4f}' for arrival_time, departure_time in finished_jobs])

    return (mrt_string, f'{dep_string}\n')


def sim(n: int, h: int, interarrival_times: Iterable[np.float64], service_times: Iterable[Iterable[np.float64]]):
    # [(job_num, sub_job_num, service_time, arrival_time)]
    high_prio_queue: list[tuple[int, int, float, float]] = []
    low_prio_queue: list[tuple[int, int, float, float]] = []

    # dict: { (job_num, sub_job_num): (remaining_service_time, arrival_time) }
    server_sub_jobs: dict[tuple[int, int], tuple[float, float]] = {}
    
    # dict: { job_num: response_time }
    job_response_times: dict[int, float] = {}

    # [(arrival_time, departure_time)]
    finished_jobs: list[tuple[float, float]] = []

    current_time = 0.00

    def is_server_full():
        if len(server_sub_jobs) > n:
            raise Exception('Server farm has too many jobs (more than possible)')
        return len(server_sub_jobs) == n

    def tick_server_sub_jobs(time_passed):
        # First: tick the time of all the jobs being processed by the server farm 
        # including removing jobs that have been completed since the last tick
        # list of items to make a copy of the dict items so we can delete from the dict as we go
        for (job_num, sub_job_num), (remaining_service_time, arrival_time) in list(sorted(server_sub_jobs.items(), key=lambda item: item[1][0])):
            tickedTime = remaining_service_time - time_passed
            # If The job has finished since the previous tick, remove it
            if (tickedTime <= 0):
                actual_departure_time = current_time + tickedTime
                finished_jobs.append((arrival_time, actual_departure_time))
                job_response_times[job_num] = (actual_departure_time - arrival_time)
                del server_sub_jobs[(job_num, sub_job_num)]
                
                if (len(high_prio_queue)):
                    job_num, sub_job_num, service_time, arrival_time = high_prio_queue.pop()
                    server_sub_jobs[(job_num, sub_job_num)] = (service_time + tickedTime, arrival_time)
                elif (len(low_prio_queue)):
                    job_num, sub_job_num, service_time, arrival_time = low_prio_queue.pop()
                    server_sub_jobs[(job_num, sub_job_num)] = (service_time + tickedTime, arrival_time)
                continue
            
            # Otherwise, tick the job by the amount of time passed
            server_sub_jobs[(job_num, sub_job_num)] = (tickedTime, arrival_time)

    for job_num, (interarrival_time, job_service_times) in enumerate(zip(interarrival_times, service_times), 1):
        
        # Tick the server farm by the time until the next event occurs (either an arrival or completion)
        target_time = current_time + interarrival_time
        stepped_time = 0.00
        # current_time < target_time but account for floating point precision error
        # https://github.com/python/peps/blob/main/peps/pep-0485.rst tolerance number derived from AA Turner
        while (target_time - current_time > 1e-8):
            times_left = [remaining for remaining, _ in server_sub_jobs.values()] + [np.inf]
            time_step = min(min(times_left), interarrival_time - stepped_time)
            stepped_time += time_step

            current_time += time_step
            tick_server_sub_jobs(time_step)

        filtered_sub_job_service_times = [service_time for service_time in job_service_times if not np.isnan(service_time)]

        num_sub_jobs = len(filtered_sub_job_service_times)
        is_high_prio = num_sub_jobs <= h

        for sub_job_num, service_time in enumerate(filtered_sub_job_service_times, 1):
            if (is_server_full()):
                if (is_high_prio):
                    high_prio_queue.insert(0, (job_num, sub_job_num, service_time, current_time))
                else:
                    low_prio_queue.insert(0, (job_num, sub_job_num, service_time, current_time))
            else:
                server_sub_jobs[(job_num, sub_job_num)] = (service_time, current_time)


    # while (len(server_sub_jobs)):
    #     for remaining_service_time, _ in list(server_sub_jobs.values()):
    #         if (not len(server_sub_jobs)):
    #             break
    #         current_time += remaining_service_time
    #         tick_server_sub_jobs(remaining_service_time)

    while (len(server_sub_jobs)):
        times_left = [remaining for remaining, _ in server_sub_jobs.values()] + [np.inf]
        time_step = min(times_left)
        current_time += time_step
        tick_server_sub_jobs(time_step)





    return format_output(np.round(np.average(list(job_response_times.values())), 4), np.round(finished_jobs, 4))
    


# inter_1_str: str = '''1.000 
# 2.000 
# 2.000 
# 1.000 
# 1.000 
# 1.000 
# 1.000 '''

# service_1_str: str = '''1.800 NaN
# 8.000  6.100
# 3.900 NaN
# 2.100  3.100
# 1.900 NaN
# 5.000  4.100
# 3.800 NaN'''

# a = sim(4, 1, np.loadtxt(io.StringIO(inter_1_str)), np.loadtxt(io.StringIO(service_1_str)))
# print(a)