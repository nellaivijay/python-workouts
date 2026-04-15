"""
Database Operations - Connection Pooling Example
"""

import sqlite3
import threading
import time
from queue import Queue
from contextlib import contextmanager
from typing import Optional
import os


class ConnectionPool:
    """Simple connection pool for SQLite"""
    
    def __init__(self, db_path: str, pool_size: int = 5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        
        # Initialize the pool with connections
        for _ in range(pool_size):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            self.pool.put(conn)
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool"""
        conn = self.pool.get()
        try:
            yield conn
        finally:
            self.pool.put(conn)
    
    def close_all(self):
        """Close all connections in the pool"""
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()


class WorkerThread(threading.Thread):
    """Worker thread that uses connection pool"""
    
    def __init__(self, pool: ConnectionPool, thread_id: int):
        super().__init__()
        self.pool = pool
        self.thread_id = thread_id
    
    def run(self):
        """Execute database operations"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            # Simulate some work
            time.sleep(0.5)
            
            # Execute query
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            
            print(f"Thread {self.thread_id}: User count = {count}")
            
            # Insert a record
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (f"User{self.thread_id}", f"user{self.thread_id}@example.com", 20 + self.thread_id)
            )
            conn.commit()
            
            print(f"Thread {self.thread_id}: Inserted user record")


def setup_database(db_path: str):
    """Setup test database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    """)
    
    # Insert some initial data
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("Alice", "alice@example.com", 28))
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("Bob", "bob@example.com", 35))
    
    conn.commit()
    conn.close()


def demonstrate_basic_pooling():
    """Demonstrate basic connection pooling"""
    db_path = "pool_example.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("Basic Connection Pooling Example")
    print("=" * 50)
    
    # Setup database
    setup_database(db_path)
    
    # Create connection pool
    pool = ConnectionPool(db_path, pool_size=3)
    
    print("\n1. Using connection pool with multiple threads:")
    
    # Create and start multiple threads
    threads = []
    for i in range(5):
        thread = WorkerThread(pool, i)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("\n2. Final user count:")
    with pool.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        final_count = cursor.fetchone()[0]
        print(f"Total users: {final_count}")
    
    # Cleanup
    pool.close_all()
    os.remove(db_path)
    print("\n3. Pool cleanup completed.")


def demonstrate_pool_efficiency():
    """Demonstrate pool efficiency vs individual connections"""
    db_path = "efficiency_test.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("\n\nPool Efficiency Comparison")
    print("=" * 50)
    
    # Setup database
    setup_database(db_path)
    
    # Test without pool
    print("\n1. Without connection pool:")
    start_time = time.time()
    
    for i in range(10):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
    
    without_pool_time = time.time() - start_time
    print(f"Time taken: {without_pool_time:.4f} seconds")
    
    # Test with pool
    print("\n2. With connection pool:")
    pool = ConnectionPool(db_path, pool_size=3)
    start_time = time.time()
    
    for i in range(10):
        with pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
    
    with_pool_time = time.time() - start_time
    print(f"Time taken: {with_pool_time:.4f} seconds")
    
    print(f"\n3. Efficiency improvement: {((without_pool_time - with_pool_time) / without_pool_time * 100):.2f}%")
    
    # Cleanup
    pool.close_all()
    os.remove(db_path)


def demonstrate_pool_limits():
    """Demonstrate pool size limits"""
    db_path = "limits_test.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("\n\nPool Size Limits Example")
    print("=" * 50)
    
    # Setup database
    setup_database(db_path)
    
    # Create pool with limited size
    pool_size = 2
    pool = ConnectionPool(db_path, pool_size=pool_size)
    
    print(f"\n1. Pool size: {pool_size}")
    print(f"2. Attempting to use more concurrent operations than pool size...")
    
    # Try to use more connections than pool size
    def worker(worker_id):
        with pool.get_connection() as conn:
            print(f"Worker {worker_id}: Acquired connection")
            time.sleep(1)
            print(f"Worker {worker_id}: Releasing connection")
    
    threads = []
    for i in range(5):  # More workers than pool size
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("\n3. All workers completed despite limited pool size")
    print("   (Connections were reused from the pool)")
    
    # Cleanup
    pool.close_all()
    os.remove(db_path)


class AdvancedConnectionPool:
    """Advanced connection pool with statistics and monitoring"""
    
    def __init__(self, db_path: str, pool_size: int = 5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        
        # Statistics
        self.total_requests = 0
        self.total_wait_time = 0
        self.active_connections = 0
        
        # Initialize pool
        for _ in range(pool_size):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            self.pool.put(conn)
    
    @contextmanager
    def get_connection(self):
        """Get connection with timing and statistics"""
        start_time = time.time()
        
        with self.lock:
            self.total_requests += 1
        
        # Wait for available connection
        conn = self.pool.get()
        wait_time = time.time() - start_time
        
        with self.lock:
            self.total_wait_time += wait_time
            self.active_connections += 1
        
        try:
            yield conn
        finally:
            with self.lock:
                self.active_connections -= 1
            self.pool.put(conn)
    
    def get_statistics(self) -> dict:
        """Get pool statistics"""
        avg_wait_time = (self.total_wait_time / self.total_requests 
                        if self.total_requests > 0 else 0)
        
        return {
            'pool_size': self.pool_size,
            'total_requests': self.total_requests,
            'active_connections': self.active_connections,
            'available_connections': self.pool.qsize(),
            'average_wait_time': avg_wait_time
        }
    
    def close_all(self):
        """Close all connections"""
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()


def demonstrate_advanced_pool():
    """Demonstrate advanced pool with monitoring"""
    db_path = "advanced_pool.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("\n\nAdvanced Connection Pool with Monitoring")
    print("=" * 50)
    
    # Setup database
    setup_database(db_path)
    
    # Create advanced pool
    pool = AdvancedConnectionPool(db_path, pool_size=3)
    
    print("\n1. Initial pool statistics:")
    print(f"   {pool.get_statistics()}")
    
    # Perform some operations
    print("\n2. Performing database operations...")
    for i in range(5):
        with pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            time.sleep(0.2)  # Simulate work
    
    print("\n3. Pool statistics after operations:")
    stats = pool.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Cleanup
    pool.close_all()
    os.remove(db_path)
    print("\n4. Advanced pool cleanup completed.")


def main():
    """Main function to run all connection pooling examples"""
    demonstrate_basic_pooling()
    demonstrate_pool_efficiency()
    demonstrate_pool_limits()
    demonstrate_advanced_pool()
    
    print("\n" + "=" * 50)
    print("Connection Pooling Key Concepts:")
    print("✓ Reuse connections to reduce overhead")
    print("✓ Limit maximum connections to prevent resource exhaustion")
    print("✓ Manage concurrent access with thread safety")
    print("✓ Monitor pool performance and statistics")
    print("✓ Implement proper connection cleanup")


if __name__ == "__main__":
    main()