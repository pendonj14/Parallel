# Analysis Questions

## 1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division.

Task Parallelism executes different tasks simultaneously on the same data.
Data Parallelism executes the same task on different data elements at the same time.

In the laboratory:

* **Part A** demonstrates **Task Parallelism** because different deduction computations run concurrently for one employee.
* **Part B** demonstrates **Data Parallelism** because the same payroll function runs simultaneously for multiple employees.

The workload division is based on whether the operations are different (tasks) or the data items are different (employees).

## 2. Explain how `concurrent.futures` managed execution, including `submit()`, `map()`, and Future objects. Discuss the purpose of `with` when creating an Executor.

`concurrent.futures` provides Executors that manage worker threads or processes.

* `submit()` schedules a function to run asynchronously and returns a Future object.
* `map()` applies a function to multiple inputs concurrently.
* **Future objects** store the result of asynchronous execution and allow retrieval using `result()`.

Using `with` ensures the executor is properly initialized and automatically shuts down after completing all tasks.

## 3. Analyze `ThreadPoolExecutor` execution in relation to the GIL and CPU cores. Did true parallelism occur?

`ThreadPoolExecutor` uses threads that share the same memory space. Because of Python’s **Global Interpreter Lock (GIL)**, only one thread executes Python bytecode at a time for CPU-bound operations.

Therefore, **true CPU parallelism does not occur**, although concurrency is still achieved for I/O-bound tasks.

## 4. Explain why `ProcessPoolExecutor` enables true parallelism, including memory space separation and GIL behavior.

`ProcessPoolExecutor` creates separate processes, each with its own memory space and independent Python interpreter. Since each process has its own **GIL**, multiple CPU cores can execute tasks simultaneously, resulting in real parallel execution.

## 5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which approach scales better and why?

**Data Parallelism using `ProcessPoolExecutor` scales better** because payroll computation for each employee can be distributed across many CPU cores.

Task Parallelism is limited since only a small fixed number of deduction tasks exist, making it less scalable as employee count increases.

## 6. Provide a real-world payroll system example. Indicate where Task Parallelism and Data Parallelism would be applied, and which executor you would use.

In a real payroll system:

* **Task Parallelism** can be used to compute different deduction types simultaneously for one employee.
* **Data Parallelism** can be used to process thousands of employee payroll records at the same time.

`ThreadPoolExecutor` would be used for deduction computations, while `ProcessPoolExecutor` would be used for processing payrolls of many employees.