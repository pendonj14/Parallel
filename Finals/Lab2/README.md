# Individual Reflections
 
## Koby Christian O. Atilano  

The most striking observation from this activity is how misleading the assumption "more cores = faster" can be. Before running the benchmarks, I expected parallel sorting to be roughly 4 times faster on large datasets since we used 4 worker processes. In reality, the speedup was barely above 1x even at one million elements, and for small datasets the parallel version was dramatically slower.
 
The sorting implementation was relatively straightforward—merge sort's recursive structure maps well onto parallel chunks. The real challenge was the merge phase after parallel sorting. Each process returns a sorted chunk, but combining four sorted lists into one globally sorted list is itself an O(n) operation that runs sequentially. This serial bottleneck limits the overall speedup, which connects directly to Amdahl's Law: the portion of work that cannot be parallelized puts a ceiling on the total improvement.
 
For searching, the results were even more eye-opening. Linear search is so fast sequentially (microseconds for small data, milliseconds for large) that spawning processes adds orders of magnitude more time than it saves. This taught me that parallelism is a tool for compute-heavy problems, not a universal accelerator. Understanding when *not* to parallelize is just as important as knowing how.

## Richter Anthony P. Yap
 
Working on the parallel search implementation gave me hands-on experience with inter-process communication, and it was more complex than I anticipated. Using `multiprocessing.Queue` to send results from workers back to the main process required careful design: each worker needs to always put something into the queue (either a found index or -1), otherwise the main process blocks forever waiting for a result that never arrives.
 
The offset calculation was another subtle point. Each worker searches a local chunk, so if it finds the target at local index 3, the global index is `offset + 3`. Getting this wrong would return incorrect positions—correctness at the coordination level, not just the algorithm level.
 
What surprised me most about the benchmark results was how the overhead of parallel searching was nearly constant (~100–400ms) regardless of dataset size. This confirms that the dominant cost is process lifecycle management, not the actual search computation. For parallelism to be worthwhile, the per-process workload needs to be substantial—on the order of seconds, not milliseconds.
 
I also gained appreciation for how Python's `multiprocessing` module handles data sharing. Data passed to workers is pickled (serialized), sent to the child process, and unpickled there. For a million-element list, this serialization cost is significant and represents pure overhead with no computational benefit.
 
## Kent John J. Chavo

My main responsibility in this project was to build and test the search algorithms. I developed sequential_search.py, which looks through data one by one, and parallel_search.py, which speeds things up by splitting the work. To make the parallel version work, I had to divide the data into four parts, give each part to a different worker process, and use a "Queue" to make sure they could send the correct result back to me. I also had to make sure my tests were fair by using the exact same data for both versions so I could see which one was actually faster.

Looking at the whole activity, I learned that there is a big difference between writing code that runs in a straight line and code that runs at the same time. While the sequential way is much easier to write and fix, the parallel way is great for handling huge amounts of data. However, I also saw that parallel code isn't always better because starting up all those processes takes extra time and effort. This project helped me understand that I need to choose the right tool based on how much data I'm dealing with and how fast the system needs to be.

## Joseph T. Pendon

This activity changed how I think about algorithm design. Before, I viewed parallelism as strictly better—why use one core when you can use four? The benchmarks conclusively demonstrated that parallelism has a break-even point, and for many practical workloads, we never reach it.
 
The implementation process also highlighted the difference between embarrassingly parallel problems and problems with dependencies. Sorting chunks independently is embarrassingly parallel—no communication is needed during the sort phase. But merging the results reintroduces a sequential dependency. Searching is similar: each chunk can be searched independently, but resolving which worker found the earliest occurrence requires coordination.
 
If I were to extend this project, I'd explore several directions: using `multiprocessing.Array` or shared memory to avoid the pickling overhead, implementing parallel merge where the merge step itself is parallelized, testing with CPU-intensive operations like matrix multiplication where parallelism shows clearer benefits, and comparing `multiprocessing` with `concurrent.futures` and `threading` to understand the trade-offs between processes and threads in Python.
 
The bottom line: parallelism is powerful but nuanced. It requires understanding both the algorithm's structure and the system's overhead characteristics to apply effectively.
