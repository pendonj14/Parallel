from concurrent.futures import ProcessPoolExecutor
import time
import os

def task(task_id):
    start = time.time()
    print(f"Task {task_id} START at {start:.2f} (PID {os.getpid()})")
    time.sleep(4)
    end = time.time()
    print(f"Task {task_id} END   at {end:.2f} (PID {os.getpid()})")

print("Parallel execution")
start_all = time.time()

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(task, range(4))

end_all = time.time()
print(f"Total time: {end_all - start_all:.2f} seconds")
