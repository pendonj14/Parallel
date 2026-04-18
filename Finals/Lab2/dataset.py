
import random


def generate_random_data(n, seed=42):
    random.seed(seed)
    return [random.randint(1, 1_000_000) for _ in range(n)]


def generate_sorted_data(n, seed=42):
    data = generate_random_data(n, seed)
    data.sort()
    return data


def generate_reverse_sorted_data(n, seed=42):

    data = generate_random_data(n, seed)
    data.sort(reverse=True)
    return data


# Predefined dataset sizes
SIZES = {
    "small": 1_000,
    "medium": 100_000,
    "large": 1_000_000,
}


if __name__ == "__main__":
    for label, size in SIZES.items():
        data = generate_random_data(size)
        print(f"{label:>8} dataset: {size:>10,} elements | "
              f"first 5: {data[:5]} | last 5: {data[-5:]}")