# Individual Reflections
 
## Koby Christian O. Atilano  

The most striking observation from this activity is how misleading the assumption "more cores = faster" can be. Before running the benchmarks, I expected parallel sorting to be roughly 4 times faster on large datasets since we used 4 worker processes. In reality, the speedup was barely above 1x even at one million elements, and for small datasets the parallel version was dramatically slower.
 
The sorting implementation was relatively straightforward—merge sort's recursive structure maps well onto parallel chunks. The real challenge was the merge phase after parallel sorting. Each process returns a sorted chunk, but combining four sorted lists into one globally sorted list is itself an O(n) operation that runs sequentially. This serial bottleneck limits the overall speedup, which connects directly to Amdahl's Law: the portion of work that cannot be parallelized puts a ceiling on the total improvement.
 
For searching, the results were even more eye-opening. Linear search is so fast sequentially (microseconds for small data, milliseconds for large) that spawning processes adds orders of magnitude more time than it saves. This taught me that parallelism is a tool for compute-heavy problems, not a universal accelerator. Understanding when *not* to parallelize is just as important as knowing how.