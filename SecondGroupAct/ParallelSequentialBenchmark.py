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