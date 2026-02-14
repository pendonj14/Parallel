import time

def task(task_id):
    start = time.time()
    print(f"Task {task_id} START at {start:.2f}")
    time.sleep(4)
    end = time.time()
    print(f'Task {task_id} END at {end:.2f}')

print("Sequential execution")
start_all = time.time()

for i in range(4):
    task(i)
    
end_all = time.time()
print(f'Total time: {end_all - start_all:.2f} seconds')