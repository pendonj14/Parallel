# Distributed Order Processing



## Reflection Questions

### 1. How did you distribute orders among worker processes?

The master uses round-robin distribution. It creates one bucket per worker, then loops through the orders assigning each one to buckets[i % num_workers]. This spreads orders evenly so no single worker gets overloaded when the count divides cleanly. Each bucket is then sent to its corresponding worker via comm.send(buckets[w - 1], dest=w, tag=0).

### 2. What happens if there are more orders than workers?

The round-robin scheme handles this naturally — workers simply receive multiple orders in their bucket and process them sequentially in a loop. For example, with 7 orders and 3 workers, the distribution becomes 3, 2, 2. Every order still gets handled; the workers with more orders just take longer to finish.

### 3. How did processing delays affect the order completion?

Each order sleeps for a random 0.5–2.0 seconds, so workers finish at unpredictable times and orders complete out of sequence. A worker assigned shorter delays finishes its whole bucket before one stuck with longer delays. This is why the master sorts by order_id at the end — the arrival order of results is not the logical order of the orders themselves.

### 4. How did you implement shared memory, and where was it initialized?

We don't use true shared memory — MPI processes have isolated address spaces, so a Manager list or lock can't be shared across them. Instead, the master keeps a local list called shared_orders, initialized as an empty list right before the collection loop. Workers build their own local results lists and send them back with comm.send(results, dest=0, tag=1). The master extends shared_orders with each incoming message. Message passing replaces shared memory.

### 5. What issues occurred when multiple workers wrote to shared memory simultaneously?

In our final design, none — because there is no shared memory to write to. Only the master writes to shared_orders, and it processes one comm.recv at a time, so concurrent writes are impossible. In an earlier version we tried using multiprocessing.Manager with a shared list and lock, but that broke entirely: Manager proxies can't be pickled across MPI processes, and even if they could, workers on different machines would have no way to reach the manager server. That experience is what pushed us toward the message-passing design.

### 6. How did you ensure consistent results when using multiple processes?

Three things working together:

- Single writer. Only the master appends to shared_orders, so there's no race condition by construction.
- Synchronous collection. The master blocks on comm.recv for every worker before printing, guaranteeing all results have arrived.
- Deterministic final ordering. Results arrive in whatever order workers finish, but sorted(shared_orders, key=lambda x: x["order_id"]) produces the same output every run regardless of timing.





