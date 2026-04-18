from multiprocessing import Pool
from sequential_sort import merge_sort, merge


def sort_chunk(chunk):
    return merge_sort(chunk)


def merge_sorted_lists(sorted_lists):
    if not sorted_lists:
        return []

    result = sorted_lists[0]
    for i in range(1, len(sorted_lists)):
        result = merge(result, sorted_lists[i])

    return result


def parallel_merge_sort(data, num_workers=4):
    n = len(data)
    if n <= 1:
        return data

    # Partition the data into chunks
    chunk_size = n // num_workers
    chunks = []
    for i in range(0, n, chunk_size):
        chunks.append(data[i:i + chunk_size])

    if len(chunks) > num_workers:
        last = chunks.pop()
        chunks[-1] = chunks[-1] + last

    # Sort each chunk in parallel
    with Pool(processes=num_workers) as pool:
        sorted_chunks = pool.map(sort_chunk, chunks)

    # Merge all sorted chunks into a single sorted list
    return merge_sorted_lists(sorted_chunks)


if __name__ == "__main__":
    import time
    from dataset import generate_random_data

    sample = generate_random_data(20, seed=99)
    print("Before:", sample)

    start = time.time()
    sorted_sample = parallel_merge_sort(sample, num_workers=4)
    end = time.time()

    print("After: ", sorted_sample)
    print(f"Time:   {end - start:.6f} seconds")

    assert sorted_sample == sorted(sample), "Parallel sort produced incorrect output!"
    print("Correctness verified.")