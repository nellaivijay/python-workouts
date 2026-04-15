"""
Performance - Profiling, Memory Management, and Caching Examples
"""

import time
import memory_profiler
import cProfile
import pstats
import io
from functools import lru_cache
from typing import Dict, Any
import sys


# Profiling Examples
def slow_function(n: int) -> int:
    """Intentionally slow function for profiling"""
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result


def fast_function(n: int) -> int:
    """Optimized version of the slow function"""
    return sum(i * j for i in range(n) for j in range(n))


def profile_functions():
    """Demonstrate profiling to identify performance bottlenecks"""
    print("Profiling Example:")
    
    # Profile slow function
    print("\nProfiling slow_function:")
    pr = cProfile.Profile()
    pr.enable()
    slow_function(100)
    pr.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    print(s.getvalue())
    
    # Profile fast function
    print("\nProfiling fast_function:")
    pr = cProfile.Profile()
    pr.enable()
    fast_function(100)
    pr.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    print(s.getvalue())


def timing_decorator(func):
    """Decorator to measure function execution time"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


@timing_decorator
def example_function(n: int) -> int:
    """Example function with timing decorator"""
    return sum(i ** 2 for i in range(n))


def timing_examples():
    """Demonstrate function timing"""
    print("\nTiming Examples:")
    
    # Manual timing
    start_time = time.time()
    result = sum(i ** 2 for i in range(1000000))
    end_time = time.time()
    print(f"Manual timing: {end_time - start_time:.4f} seconds")
    
    # Decorator timing
    example_function(1000000)


# Memory Management Examples
def memory_intensive_function():
    """Function that uses significant memory"""
    large_list = [i for i in range(1000000)]
    return sum(large_list)


def memory_efficient_function():
    """Memory-efficient version using generator"""
    return sum(i for i in range(1000000))


def demonstrate_memory_usage():
    """Demonstrate memory profiling"""
    print("\nMemory Usage Examples:")
    
    print("Memory-intensive function:")
    mem_usage = memory_profiler.memory_usage(memory_intensive_function)
    print(f"  Memory used: {mem_usage:.2f} MiB")
    
    print("\nMemory-efficient function:")
    mem_usage = memory_profiler.memory_usage(memory_efficient_function)
    print(f"  Memory used: {mem_usage:.2f} MiB")


def generator_example():
    """Demonstrate memory-efficient generators"""
    print("\nGenerator vs List Example:")
    
    # List approach (memory intensive)
    start_time = time.time()
    numbers_list = [i ** 2 for i in range(1000000)]
    list_memory = sys.getsizeof(numbers_list) / (1024 * 1024)
    list_time = time.time() - start_time
    
    # Generator approach (memory efficient)
    start_time = time.time()
    numbers_generator = (i ** 2 for i in range(1000000))
    generator_sum = sum(numbers_generator)
    generator_time = time.time() - start_time
    
    print(f"  List: {list_memory:.2f} MiB, {list_time:.4f}s")
    print(f"  Generator: Minimal memory, {generator_time:.4f}s")


def context_manager_example():
    """Demonstrate resource management with context managers"""
    print("\nContext Manager Example:")
    
    class ResourceManager:
        """Custom context manager for resource cleanup"""
        def __init__(self, resource_name):
            self.resource_name = resource_name
        
        def __enter__(self):
            print(f"  Acquiring {self.resource_name}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"  Releasing {self.resource_name}")
            return False
    
    with ResourceManager("database connection"):
        print("  Using resource...")


# Caching Examples
@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    """Expensive computation with caching"""
    print(f"  Computing for {n}")
    time.sleep(0.1)  # Simulate expensive operation
    return n * n


def demonstrate_caching():
    """Demonstrate memoization and caching"""
    print("\nCaching Example:")
    
    print("First call (computes):")
    result1 = expensive_computation(5)
    print(f"  Result: {result1}")
    
    print("\nSecond call (uses cache):")
    result2 = expensive_computation(5)
    print(f"  Result: {result2}")
    
    print(f"\nCache info: {expensive_computation.cache_info()}")


class SimpleCache:
    """Simple in-memory cache implementation"""
    
    def __init__(self, max_size: int = 100):
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.access_count: Dict[str, int] = {}
    
    def get(self, key: str) -> Any:
        """Get value from cache"""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        if len(self.cache) >= self.max_size:
            # Remove least recently used item
            lru_key = min(self.access_count, key=self.access_count.get)
            del self.cache[lru_key]
            del self.access_count[lru_key]
        
        self.cache[key] = value
        self.access_count[key] = 0
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.access_count.clear()


def demonstrate_custom_cache():
    """Demonstrate custom cache implementation"""
    print("\nCustom Cache Example:")
    
    cache = SimpleCache(max_size=3)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    
    print(f"  Cache size: {len(cache.cache)}")
    print(f"  Get key1: {cache.get('key1')}")
    
    cache.set("key4", "value4")  # Should evict least recently used
    print(f"  Cache size after adding key4: {len(cache.cache)}")
    print(f"  key1 still in cache: {cache.get('key1') is not None}")


def optimization_strategies():
    """Demonstrate various optimization strategies"""
    print("\nOptimization Strategies:")
    
    # String concatenation
    print("String concatenation:")
    
    start_time = time.time()
    result = ""
    for i in range(10000):
        result += str(i)
    concat_time = time.time() - start_time
    
    start_time = time.time()
    result_list = []
    for i in range(10000):
        result_list.append(str(i))
    result = "".join(result_list)
    join_time = time.time() - start_time
    
    print(f"  Concatenation: {concat_time:.4f}s")
    print(f"  Join method: {join_time:.4f}s")
    print(f"  Speedup: {concat_time/join_time:.2f}x")
    
    # List vs set for membership testing
    print("\nMembership testing:")
    
    large_list = list(range(100000))
    large_set = set(large_list)
    
    start_time = time.time()
    _ = 99999 in large_list
    list_time = time.time() - start_time
    
    start_time = time.time()
    _ = 99999 in large_set
    set_time = time.time() - start_time
    
    print(f"  List: {list_time:.6f}s")
    print(f"  Set: {set_time:.6f}s")
    print(f"  Speedup: {list_time/set_time:.2f}x")


def main():
    """Main function to demonstrate performance concepts"""
    print("Performance Examples")
    print("=" * 50)
    
    # Profiling
    profile_functions()
    timing_examples()
    
    # Memory management
    demonstrate_memory_usage()
    generator_example()
    context_manager_example()
    
    # Caching
    demonstrate_caching()
    demonstrate_custom_cache()
    
    # Optimization strategies
    optimization_strategies()
    
    print("\n" + "=" * 50)
    print("Performance Key Concepts:")
    print("✓ Profiling: Identify bottlenecks with cProfile")
    print("✓ Timing: Measure execution time accurately")
    print("✓ Memory Management: Use generators, context managers")
    print("✓ Caching: Memoization to avoid redundant computations")
    print("✓ Optimization: Choose right data structures and algorithms")
    print("✓ Resource Management: Proper cleanup with context managers")
    print("\nOptimization Tips:")
    print("• Profile before optimizing")
    print("• Use generators for large datasets")
    print("• Choose appropriate data structures")
    print("• Implement caching for expensive operations")
    print("• Use built-in functions and libraries")
    print("• Consider algorithmic complexity")
    print("\nTo run this script:")
    print("pip install memory-profiler")


if __name__ == "__main__":
    main()