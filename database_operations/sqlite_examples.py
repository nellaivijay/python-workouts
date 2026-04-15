"""
Database Operations - SQLite Examples
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Optional, Any
import os


@contextmanager
def get_db_connection(db_path: str):
    """Context manager for database connections"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()


def create_database_schema(conn):
    """Create database tables"""
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT,
            stock INTEGER DEFAULT 0
        )
    """)
    
    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)
    
    conn.commit()
    print("Database schema created successfully.")


def insert_user(conn, name: str, email: str, age: Optional[int] = None):
    """Insert a new user"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        (name, email, age)
    )
    conn.commit()
    print(f"User '{name}' inserted with ID: {cursor.lastrowid}")
    return cursor.lastrowid


def insert_product(conn, name: str, price: float, category: str, stock: int = 0):
    """Insert a new product"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, category, stock) VALUES (?, ?, ?, ?)",
        (name, price, category, stock)
    )
    conn.commit()
    print(f"Product '{name}' inserted with ID: {cursor.lastrowid}")
    return cursor.lastrowid


def insert_order(conn, user_id: int, product_id: int, quantity: int):
    """Insert a new order"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
        (user_id, product_id, quantity)
    )
    conn.commit()
    print(f"Order inserted with ID: {cursor.lastrowid}")
    return cursor.lastrowid


def get_all_users(conn) -> List[Dict]:
    """Retrieve all users"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return [dict(row) for row in cursor.fetchall()]


def get_user_by_id(conn, user_id: int) -> Optional[Dict]:
    """Get a specific user by ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_users_with_orders(conn) -> List[Dict]:
    """Get users with their order counts using JOIN"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.*, COUNT(o.id) as order_count
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        GROUP BY u.id
    """)
    return [dict(row) for row in cursor.fetchall()]


def update_user_email(conn, user_id: int, new_email: str):
    """Update user email"""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    conn.commit()
    print(f"User {user_id} email updated to {new_email}")


def delete_user(conn, user_id: int):
    """Delete a user"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    print(f"User {user_id} deleted")


def search_products(conn, search_term: str, min_price: Optional[float] = None) -> List[Dict]:
    """Search products with optional price filter"""
    cursor = conn.cursor()
    
    if min_price:
        cursor.execute(
            "SELECT * FROM products WHERE name LIKE ? AND price >= ?",
            (f"%{search_term}%", min_price)
        )
    else:
        cursor.execute(
            "SELECT * FROM products WHERE name LIKE ?",
            (f"%{search_term}%",)
        )
    
    return [dict(row) for row in cursor.fetchall()]


def get_aggregated_data(conn) -> Dict:
    """Get aggregated statistics"""
    cursor = conn.cursor()
    
    # User statistics
    cursor.execute("SELECT COUNT(*) as total_users, AVG(age) as avg_age FROM users")
    user_stats = dict(cursor.fetchone())
    
    # Product statistics
    cursor.execute("SELECT COUNT(*) as total_products, AVG(price) as avg_price FROM products")
    product_stats = dict(cursor.fetchone())
    
    # Order statistics
    cursor.execute("SELECT COUNT(*) as total_orders, SUM(quantity) as total_items FROM orders")
    order_stats = dict(cursor.fetchone())
    
    return {
        'users': user_stats,
        'products': product_stats,
        'orders': order_stats
    }


def execute_transaction(conn):
    """Demonstrate transaction handling"""
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN TRANSACTION")
        
        # Multiple operations
        cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = 1")
        cursor.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (1, 1, 1)")
        
        # Commit transaction
        conn.commit()
        print("Transaction completed successfully")
        
    except Exception as e:
        # Rollback on error
        conn.rollback()
        print(f"Transaction failed and rolled back: {e}")


def backup_database(conn, backup_path: str):
    """Create a backup of the database"""
    with open(backup_path, 'w') as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")
    print(f"Database backed up to {backup_path}")


def main():
    """Main function to demonstrate SQLite operations"""
    db_path = "example.db"
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("SQLite Database Operations Example")
    print("=" * 50)
    
    with get_db_connection(db_path) as conn:
        # Create schema
        print("\n1. Creating database schema:")
        create_database_schema(conn)
        
        # Insert sample data
        print("\n2. Inserting sample data:")
        user1_id = insert_user(conn, "Alice Johnson", "alice@example.com", 28)
        user2_id = insert_user(conn, "Bob Smith", "bob@example.com", 35)
        user3_id = insert_user(conn, "Charlie Brown", "charlie@example.com", 42)
        
        product1_id = insert_product(conn, "Laptop", 999.99, "Electronics", 50)
        product2_id = insert_product(conn, "Mouse", 29.99, "Electronics", 200)
        product3_id = insert_product(conn, "Desk Chair", 199.99, "Furniture", 30)
        
        # Insert orders
        print("\n3. Creating orders:")
        insert_order(conn, user1_id, product1_id, 1)
        insert_order(conn, user1_id, product2_id, 2)
        insert_order(conn, user2_id, product1_id, 1)
        insert_order(conn, user3_id, product3_id, 3)
        
        # Query data
        print("\n4. Querying data:")
        print("All users:")
        for user in get_all_users(conn):
            print(f"  {user}")
        
        print(f"\nUser by ID {user1_id}:")
        print(f"  {get_user_by_id(conn, user1_id)}")
        
        print("\nUsers with order counts:")
        for user in get_users_with_orders(conn):
            print(f"  {user['name']}: {user['order_count']} orders")
        
        # Search products
        print("\n5. Searching products:")
        print("Products containing 'top':")
        for product in search_products(conn, "top"):
            print(f"  {product['name']}: ${product['price']}")
        
        # Update data
        print("\n6. Updating data:")
        update_user_email(conn, user1_id, "alice.new@example.com")
        
        # Get aggregated data
        print("\n7. Aggregated statistics:")
        stats = get_aggregated_data(conn)
        for category, data in stats.items():
            print(f"  {category}: {data}")
        
        # Transaction example
        print("\n8. Transaction example:")
        execute_transaction(conn)
        
        # Backup
        print("\n9. Creating backup:")
        backup_database(conn, "database_backup.sql")
    
    # Cleanup
    os.remove(db_path)
    os.remove("database_backup.sql")
    print("\n10. Cleanup completed.")


if __name__ == "__main__":
    main()