import time
import random
from mpi4py import MPI


def generate_orders(n):
    items = ["Burger", "Pizza", "Pasta", "Salad", "Sushi",
             "Tacos", "Ramen", "Sandwich", "Steak", "Soup"]
    return [{"order_id": 1000 + i, "item": random.choice(items)}
            for i in range(n)]


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        if rank == 0:
            print("Run with at least 2 processes.")
        return

    if rank == 0:
        num_orders = random.randint(5, 8)
        orders = generate_orders(num_orders)
        print(f"[Master] Generated {num_orders} orders\n")

        num_workers = size - 1
        buckets = [[] for _ in range(num_workers)]
        for i, order in enumerate(orders):
            buckets[i % num_workers].append(order)

        for w in range(1, size):
            comm.send(buckets[w - 1], dest=w, tag=0)

        # wait for all workers to finish
        for w in range(1, size):
            comm.recv(source=w, tag=1)

        print("\n[Master] All workers finished.")

    else:
        my_orders = comm.recv(source=0, tag=0)
        print(f"[Worker {rank}] Received {len(my_orders)} order(s)")

        for order in my_orders:
            delay = random.uniform(0.5, 2.0)
            print(f"[Worker {rank}] Processing Order {order['order_id']} "
                  f"({order['item']}) — {delay:.2f}s")
            time.sleep(delay)
            print(f"[Worker {rank}] Finished Order {order['order_id']}")

        comm.send("done", dest=0, tag=1)

if __name__ == "__main__":
    main()
