def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1


if __name__ == "__main__":
    import time
    from dataset import generate_random_data

    data = generate_random_data(100_000)

    target_present = data[50_000]
    target_absent = -1

    start = time.time()
    idx = linear_search(data, target_present)
    end = time.time()
    print(f"Found {target_present} at index {idx} in {end - start:.6f}s")

    start = time.time()
    idx = linear_search(data, target_absent)
    end = time.time()
    print(f"Search for {target_absent}: index {idx} in {end - start:.6f}s")