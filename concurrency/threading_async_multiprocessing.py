"""
Concurrency - Threading, Async/Await, and Multiprocessing Examples
"""

import threading
import asyncio
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List


def simulate_io_task(task_id: int, duration: float = 1.0) -> str:
    """Simulate an I/O-bound task"""
    time.sleep(duration)
    return f"Task {task_id} completed after {duration} seconds"


def simulate_cpu_task(n: int) -> int:
    """Simulate a CPU-bound task"""
    result = sum(i * i for i in range(n))
    return result


# Threading Examples
def run_threading_example():
    """Demonstrate threading for I/O-bound tasks"""
    print("Threading Example (I/O-bound tasks):")
    
    start_time = time.time()
    
    # Sequential execution
    print("\nSequential execution:")
    sequential_start = time.time()
    for i in range(3):
        result = simulate_io_task(i, 0.5)
        print(f"  {result}")
    sequential_time = time.time() - sequential_start
    
    # Threaded execution
    print("\nThreaded execution:")
    threaded_start = time.time()
    threads = []
    
    for i in range(3):
        thread = threading.Thread(target=simulate_io_task, args=(i, 0.5))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    threaded_time = time.time() - threaded_start
    
    print(f"\nSequential time: {sequential_time:.2f}s")
    print(f"Threaded time: {threaded_time:.2f}s")
    print(f"Speedup: {sequential_time/threaded_time:.2f}x")


def run_thread_pool_executor():
    """Demonstrate ThreadPoolExecutor"""
    print("\nThreadPoolExecutor Example:")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(simulate_io_task, i, 0.5) for i in range(3)]
        
        for future in futures:
            print(f"  {future.result()}")


# Async/Await Examples
async def async_io_task(task_id: int, duration: float = 1.0) -> str:
    """Simulate an async I/O task"""
    await asyncio.sleep(duration)
    return f"Async task {task_id} completed after {duration} seconds"


async def run_async_example():
    """Demonstrate async/await for I/O-bound tasks"""
    print("\nAsync/Await Example:")
    
    start_time = time.time()
    
    # Run tasks concurrently
    tasks = [async_io_task(i, 0.5) for i in range(3)]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"  {result}")
    
    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f}s")


async def async_with_timeout():
    """Demonstrate async with timeout"""
    print("\nAsync with Timeout Example:")
    
    try:
        result = await asyncio.wait_for(async_io_task(1, 2.0), timeout=1.0)
        print(f"  Task completed: {result}")
    except asyncio.TimeoutError:
        print("  Task timed out after 1.0 second")


# Multiprocessing Examples
def run_multiprocessing_example():
    """Demonstrate multiprocessing for CPU-bound tasks"""
    print("\nMultiprocessing Example (CPU-bound tasks):")
    
    # Sequential execution
    print("\nSequential execution:")
    sequential_start = time.time()
    results = [simulate_cpu_task(1000000) for _ in range(3)]
    sequential_time = time.time() - sequential_start
    print(f"  Results: {results}")
    print(f"  Time: {sequential_time:.2f}s")
    
    # Multiprocessing execution
    print("\nMultiprocessing execution:")
    mp_start = time.time()
    
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(simulate_cpu_task, [1000000] * 3)
    
    mp_time = time.time() - mp_start
    print(f"  Results: {results}")
    print(f"  Time: {mp_time:.2f}s")
    print(f"  Speedup: {sequential_time/mp_time:.2f}x")


def run_process_pool_executor():
    """Demonstrate ProcessPoolExecutor"""
    print("\nProcessPoolExecutor Example:")
    
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(simulate_cpu_task, 1000000) for _ in range(3)]
        
        results = [future.result() for future in futures]
        print(f"  Results: {results}")


# Shared Data and Synchronization
class SharedCounter:
    """Thread-safe counter using locks"""
    
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self):
        """Thread-safe increment"""
        with self.lock:
            self.value += 1
            return self.value


def demonstrate_thread_safety():
    """Demonstrate thread safety with locks"""
    print("\nThread Safety Example:")
    
    counter = SharedCounter()
    
    def increment_counter(times: int):
        for _ in range(times):
            counter.increment()
    
    # Create multiple threads
    threads = [threading.Thread(target=increment_counter, args=(1000,)) for _ in range(5)]
    
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"  Final counter value: {counter.value}")
    print(f"  Expected value: {5 * 1000}")
    print(f"  Time: {time.time() - start_time:.2f}s")


# Producer-Consumer Pattern
def producer_consumer_example():
    """Demonstrate producer-consumer pattern with queue"""
    print("\nProducer-Consumer Example:")
    
    import queue
    
    q = queue.Queue(maxsize=5)
    
    def producer():
        for i in range(10):
            q.put(f"Item {i}")
            print(f"  Produced: Item {i}")
            time.sleep(0.1)
    
    def consumer():
        while True:
            try:
                item = q.get(timeout=1)
                print(f"  Consumed: {item}")
                q.task_done()
            except queue.Empty:
                break
    
    # Start producer and consumer threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()


async def main_async():
    """Main async function"""
    await run_async_example()
    await async_with_timeout()


def main():
    """Main function to demonstrate concurrency concepts"""
    print("Concurrency Examples")
    print("=" * 50)
    
    # Threading examples
    run_threading_example()
    run_thread_pool_executor()
    
    # Async/await examples
    print("\nRunning Async Examples:")
    asyncio.run(main_async())
    
    # Multiprocessing examples
    run_multiprocessing_example()
    run_process_pool_executor()
    
    # Synchronization examples
    demonstrate_thread_safety()
    producer_consumer_example()
    
    print("\n" + "=" * 50)
    print("Concurrency Key Concepts:")
    print("✓ Threading: I/O-bound tasks, shared memory")
    print("✓ Async/Await: Non-blocking I/O, event loop")
    print("✓ Multiprocessing: CPU-bound tasks, separate memory")
    print("✓ Thread Safety: Locks, queues, synchronization")
    print("✓ Executors: High-level pool management")
    print("✓ Producer-Consumer: Inter-thread communication")
    print("\nUse Cases:")
    print("• Threading: Web scraping, file I/O, network requests")
    print("• Async: Web servers, database queries, real-time data")
    print("• Multiprocessing: Data processing, computation, ML training")


if __name__ == "__main__":
    main()