from multiprocessing import Process, Queue


def worker(sub_data, target, q, offset):
    for i in range(len(sub_data)):
        if sub_data[i] == target:
            q.put(offset + i)
            return
    q.put(-1)


def parallel_linear_search(data, target, num_workers=4):
    n = len(data)
    chunk_size = n // num_workers
    processes = []
    result_queue = Queue()

    for i in range(num_workers):
        start_idx = i * chunk_size
        if i == num_workers - 1:
            end_idx = n
        else:
            end_idx = start_idx + chunk_size

        chunk = data[start_idx:end_idx]
        p = Process(target=worker, args=(chunk, target, result_queue, start_idx))
        processes.append(p)
        p.start()

    results = []
    for _ in processes:
        results.append(result_queue.get())

    for p in processes:
        p.join()

    found_indices = [r for r in results if r != -1]
    if found_indices:
        return min(found_indices)
    return -1


if __name__ == "__main__":
    import time
    from dataset import generate_random_data

    data = generate_random_data(100_000)

    target_present = data[50_000]
    target_absent = -1

    start = time.time()
    idx = parallel_linear_search(data, target_present, num_workers=4)
    end = time.time()
    print(f"Found {target_present} at index {idx} in {end - start:.6f}s")

    start = time.time()
    idx = parallel_linear_search(data, target_absent, num_workers=4)
    end = time.time()
    print(f"Search for {target_absent}: index {idx} in {end - start:.6f}s")