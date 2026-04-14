import time
import random
from multiprocessing import Pool, cpu_count, Lock


lock = Lock()

def process_request(request_id):
    computation = 0
    for _ in range(80000):
        computation += random.randint(1, 5)

    with lock:
        saved_record = computation * 2

    return saved_record

def sequential_processing(requests):
    results = []
    for req in requests:
        results.append(process_request(req))
    return results

def parallel_processing(requests):
    with Pool(cpu_count()) as pool:
        results = pool.map(process_request, requests)
    return results

if __name__ == "__main__":

    # Simulate 300 students in queue
    requests = list(range(300))

    # Sequential execution
    start_seq = time.time()
    sequential_processing(requests)
    end_seq = time.time()
    sequential_time = end_seq - start_seq

    # Parallel execution
    start_par = time.time()
    parallel_processing(requests)
    end_par = time.time()
    parallel_time = end_par - start_par

    # Speedup calculation
    speedup = sequential_time / parallel_time

    print("Sequential Time:", round(sequential_time, 4), "seconds")
    print("Parallel Time:", round(parallel_time, 4), "seconds")
    print("Speedup:", round(speedup, 4), "x")
    print("CPU Cores Used:", cpu_count())