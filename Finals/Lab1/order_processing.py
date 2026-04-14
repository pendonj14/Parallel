import time
import random
from mpi4py import MPI
from multiprocessing import Manager


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

    manager = Manager()
    shared_orders = manager.list()

    if rank == 0:
        num_orders = random.randint(5, 8)
        orders = generate_orders(num_orders)
        print(f"[Master] Generated {num_orders} orders\n")

        num_workers = size - 1
        buckets = [[] for _ in range(num_workers)]
        for i, order in enumerate(orders):
            buckets[i % num_workers].append(order)

        for w in range(1, size):
            comm.send(
                {"orders": buckets[w - 1], "shared_orders": shared_orders},
                dest=w, tag=0,
            )

        for w in range(1, size):
            comm.recv(source=w, tag=1)

        print("\n========== COMPLETED ORDERS ==========")
        for o in list(shared_orders):
            print(f"  Order {o['order_id']} | {o['item']} | Worker {o['handled_by']}")
        print(f"Total: {len(shared_orders)}/{num_orders}")
        print("======================================")

    else:
        payload = comm.recv(source=0, tag=0)
        my_orders = payload["orders"]
        shared_orders = payload["shared_orders"]

        print(f"[Worker {rank}] Received {len(my_orders)} order(s)")

        for order in my_orders:
            delay = random.uniform(0.5, 2.0)
            print(f"[Worker {rank}] Processing Order {order['order_id']} "
                  f"({order['item']}) — {delay:.2f}s")
            time.sleep(delay)

            completed = {
                "order_id": order["order_id"],
                "item": order["item"],
                "handled_by": rank,
                "duration": round(delay, 2),
            }
            # NO LOCK YET — race condition possible
            shared_orders.append(completed)

            print(f"[Worker {rank}] Finished Order {order['order_id']}")

        comm.send("done", dest=0, tag=1)


if __name__ == "__main__":
    main()