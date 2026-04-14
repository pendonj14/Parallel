# Lab Report: Multithreading and Multiprocessing in Python

**Date:** February 7, 2026  
**Name of Each Member:**
* Atilano, Koby Christian  
* Chavo, Kent John  
* Pendon, Joseph Jr.  
* Yap, Richter Anthony  

**Course:** CS323 - Parallel and Distributed Computing  
**Instructor:** Raniah L. Taurac  

---

**1. Which approach demonstrates true parallelism in Python? Explain.** Multiprocessing demonstrates true parallelism. In the provided code, each grade is passed to a separate `Process`, which runs in its own memory space and instance of the Python interpreter. This allows the operating system to execute these processes simultaneously across multiple CPU cores, bypassing the limitations of a single core.



**2. Compare execution times between multithreading and multiprocessing.** Multithreading is generally faster for this specific task. Because the code creates a new thread or process for every single subject grade entered, the "overhead" or startup time becomes the main factor. Processes are heavy and take more time for the operating system to create and manage, whereas threads are lightweight and start almost instantly. Since the mathematical calculation is very simple, the time spent setting up processes makes multiprocessing slower overall.

**3. Can Python handle true parallelism using threads? Why or why not?** Python cannot handle true parallelism using threads for CPU-bound tasks. This is due to the Global Interpreter Lock (GIL), which ensures that only one thread executes Python code at a time. While the threads in the code appear to run together and print results in a random order, they are actually taking turns very rapidly on a single CPU core rather than running truly in parallel at the hardware level.



**4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?** If 1,000 grades are entered, the code will attempt to spawn 1,000 separate threads or processes. Multithreading would be the faster and more stable method. Creating 1,000 processes would likely overwhelm the system's memory and CPU resources due to the high cost of process creation and context switching. Threads share the same memory space and require much fewer resources, making them more efficient for handling a high volume of these small, quick tasks.

**5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?** Multiprocessing is better for CPU-bound tasks, such as heavy mathematical calculations or data processing, because it can utilize multiple cores. Multithreading is better for I/O-bound tasks, such as waiting for user input or reading files, as it allows the program to stay responsive while waiting for external operations to complete.

**6. How did your group apply creative coding or algorithmic solutions in this lab?** The group applied creative coding by implementing a dynamic input system. Instead of using a fixed list of grades, the code uses a loop that allows the user to specify the exact number of subjects and input grades in real-time. Additionally, the worker functions were designed to handle these inputs independently and provide clear, tagged output (e.g., `[Process]` or `[Thread]`) to easily distinguish and observe the execution behavior of each method.




# Execution Time Comparison: Multithreading vs Multiprocessing (Number 3)

## Execution Results

The `time` module was used to measure the execution time of both implementations.  
Each grade was processed independently using threads or processes.

| Method | Execution Order | GWA Output | Execution Time |
|------|----------------|------------|----------------|
| Multithreading | Non-deterministic (varies per run) | Individual GWA per subject printed by threads | Faster startup, lower overhead |
| Multiprocessing | Non-deterministic (varies per run) | Individual GWA per subject printed by processes | Slower startup, higher overhead |

---

## Discussion

### Why outputs may appear in different order
Both multithreading and multiprocessing execute tasks concurrently.  
The operating system scheduler decides when each thread or process runs, so there is **no guaranteed execution order**. As a result, output lines may appear in a different order every time the program runs.

In multithreading, threads share the same memory space and run within a single process, which makes them lightweight but still subject to scheduling.  
In multiprocessing, each process runs independently with its own memory, leading to even more variability in execution order.

---

## Optimization Ideas

- **For faster execution:**
  - Use multithreading for I/O-bound tasks (e.g., input/output operations).
  - Use multiprocessing for CPU-bound tasks that require true parallelism.

- **For better readability:**
  - Separate input collection from computation logic.
  - Use descriptive function names and consistent formatting.
  - Add minimal comments to explain thread/process behavior.

---

## Conclusion

Multithreading has lower overhead and faster startup time, while multiprocessing provides true parallelism at the cost of higher resource usage. Both approaches demonstrate concurrent execution, as shown by the varying execution order of outputs.


