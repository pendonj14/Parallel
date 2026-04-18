
def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left_half = merge_sort(data[:mid])
    right_half = merge_sort(data[mid:])

    return merge(left_half, right_half)


if __name__ == "__main__":
    import time
    from dataset import generate_random_data

    sample = generate_random_data(20, seed=99)
    print("Before:", sample)

    start = time.time()
    sorted_sample = merge_sort(sample)
    end = time.time()

    print("After: ", sorted_sample)
    print(f"Time:   {end - start:.6f} seconds")

    # Verify correctness
    assert sorted_sample == sorted(sample), "Sort produced incorrect output!"
    print("Correctness verified.")