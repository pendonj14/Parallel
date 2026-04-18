import time
import sys
from dataset import (
    generate_random_data,
    generate_sorted_data,
    generate_reverse_sorted_data,
    SIZES,
)
from sequential_sort import merge_sort
from parallel_sort import parallel_merge_sort
from sequential_search import linear_search
from parallel_search import parallel_linear_search


def time_it(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start


def benchmark_sorting(data, label):
    print(f"\n  [{label}] size = {len(data):>10,}")

    data_copy1 = data[:]
    data_copy2 = data[:]

    sorted_seq, t_seq = time_it(merge_sort, data_copy1)
    print(f"    Sequential Merge Sort : {t_seq:>10.4f}s")

    sorted_par, t_par = time_it(parallel_merge_sort, data_copy2, 4)
    print(f"    Parallel   Merge Sort : {t_par:>10.4f}s")

    speedup = t_seq / t_par if t_par > 0 else float("inf")
    print(f"    Speedup (seq/par)     : {speedup:>10.2f}x")

    # Verify correctness
    expected = sorted(data)
    assert sorted_seq == expected, "Sequential sort FAILED correctness check!"
    assert sorted_par == expected, "Parallel sort FAILED correctness check!"
    print(f"    Correctness           : PASS")

    return t_seq, t_par


def benchmark_searching(data, label):
    """Benchmark sequential and parallel linear search on the given data."""
    print(f"\n  [{label}] size = {len(data):>10,}")

    target = data[len(data) // 2]

    idx_seq, t_seq = time_it(linear_search, data, target)
    print(f"    Sequential Linear Search : {t_seq:>10.6f}s  (index={idx_seq})")

    idx_par, t_par = time_it(parallel_linear_search, data, target, 4)
    print(f"    Parallel   Linear Search : {t_par:>10.6f}s  (index={idx_par})")

    speedup = t_seq / t_par if t_par > 0 else float("inf")
    print(f"    Speedup (seq/par)        : {speedup:>10.4f}x")

    # Verify correctness
    assert data[idx_seq] == target, "Sequential search returned wrong index!"
    assert data[idx_par] == target, "Parallel search returned wrong index!"
    print(f"    Correctness              : PASS")

    # Also test target-not-found
    missing = -999
    idx_seq_nf, _ = time_it(linear_search, data, missing)
    idx_par_nf, _ = time_it(parallel_linear_search, data, missing, 4)
    assert idx_seq_nf == -1, "Sequential search should return -1 for missing target!"
    assert idx_par_nf == -1, "Parallel search should return -1 for missing target!"
    print(f"    Not-found case           : PASS")

    return t_seq, t_par


def main():
    print("=" * 65)
    print("  SEQUENTIAL vs PARALLEL ALGORITHM BENCHMARK")
    print("=" * 65)

    #SORTING BENCHMARKS
    print("\n" + "=" * 65)
    print("  SORTING BENCHMARKS")
    print("=" * 65)

    sort_results = {}
    for label, n in SIZES.items():
        data = generate_random_data(n)
        t_seq, t_par = benchmark_sorting(data, f"Random - {label}")
        sort_results[f"random_{label}"] = (t_seq, t_par)

    # already sorted data (large)
    data_sorted = generate_sorted_data(SIZES["large"])
    t_seq, t_par = benchmark_sorting(data_sorted, "Already Sorted - large")
    sort_results["sorted_large"] = (t_seq, t_par)

    # reverse sorted data (large)
    data_reverse = generate_reverse_sorted_data(SIZES["large"])
    t_seq, t_par = benchmark_sorting(data_reverse, "Reverse Sorted - large")
    sort_results["reverse_large"] = (t_seq, t_par)

    # SEARCHING BENCHMARKS 
    print("\n" + "=" * 65)
    print("  SEARCHING BENCHMARKS")
    print("=" * 65)

    search_results = {}
    for label, n in SIZES.items():
        data = generate_random_data(n)
        t_seq, t_par = benchmark_searching(data, f"Random - {label}")
        search_results[f"random_{label}"] = (t_seq, t_par)

    # searching in sorted data
    data_sorted = generate_sorted_data(SIZES["large"])
    t_seq, t_par = benchmark_searching(data_sorted, "Sorted - large")
    search_results["sorted_large"] = (t_seq, t_par)

    # SUMMARY TABLE 
    print("\n" + "=" * 65)
    print("  SUMMARY")
    print("=" * 65)

    print(f"\n  {'Test Case':<30} {'Sequential':>12} {'Parallel':>12} {'Speedup':>10}")
    print("  " + "-" * 64)

    print("\n  Sorting:")
    for key, (ts, tp) in sort_results.items():
        sp = ts / tp if tp > 0 else float("inf")
        print(f"    {key:<28} {ts:>11.4f}s {tp:>11.4f}s {sp:>9.2f}x")

    print("\n  Searching:")
    for key, (ts, tp) in search_results.items():
        sp = ts / tp if tp > 0 else float("inf")
        print(f"    {key:<28} {ts:>11.6f}s {tp:>11.6f}s {sp:>9.4f}x")

    print("\n" + "=" * 65)
    print("  All correctness checks PASSED.")
    print("=" * 65)


if __name__ == "__main__":
    main()