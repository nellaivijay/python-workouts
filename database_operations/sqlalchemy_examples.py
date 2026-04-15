"""
Database Operations - SQLAlchemy ORM Examples
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Product(Base):
    """Product model"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50))
    stock = Column(Integer, default=0)
    
    # Relationships
    orders = relationship("Order", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


class Order(Base):
    """Order model"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"


class DatabaseManager:
    """Database manager class for SQLAlchemy operations"""
    
    def __init__(self, db_path: str = "sqlalchemy_example.db"):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.engine)
        print("Database tables created successfully.")
    
    def drop_tables(self):
        """Drop all tables from the database"""
        Base.metadata.drop_all(self.engine)
        print("Database tables dropped.")
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def add_user(self, name: str, email: str, age: int = None) -> User:
        """Add a new user"""
        session = self.get_session()
        try:
            user = User(name=name, email=email, age=age)
            session.add(user)
            session.commit()
            print(f"User '{name}' added with ID: {user.id}")
            return user
        except Exception as e:
            session.rollback()
            print(f"Error adding user: {e}")
            return None
        finally:
            session.close()
    
    def add_product(self, name: str, price: float, category: str = None, stock: int = 0) -> Product:
        """Add a new product"""
        session = self.get_session()
        try:
            product = Product(name=name, price=price, category=category, stock=stock)
            session.add(product)
            session.commit()
            print(f"Product '{name}' added with ID: {product.id}")
            return product
        except Exception as e:
            session.rollback()
            print(f"Error adding product: {e}")
            return None
        finally:
            session.close()
    
    def add_order(self, user_id: int, product_id: int, quantity: int) -> Order:
        """Add a new order"""
        session = self.get_session()
        try:
            order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
            session.add(order)
            session.commit()
            print(f"Order added with ID: {order.id}")
            return order
        except Exception as e:
            session.rollback()
            print(f"Error adding order: {e}")
            return None
        finally:
            session.close()
    
    def get_all_users(self) -> list:
        """Get all users"""
        session = self.get_session()
        try:
            users = session.query(User).all()
            return users
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        finally:
            session.close()
    
    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.email == email).first()
            return user
        finally:
            session.close()
    
    def get_products_by_category(self, category: str) -> list:
        """Get products by category"""
        session = self.get_session()
        try:
            products = session.query(Product).filter(Product.category == category).all()
            return products
        finally:
            session.close()
    
    def get_products_in_price_range(self, min_price: float, max_price: float) -> list:
        """Get products within price range"""
        session = self.get_session()
        try:
            products = session.query(Product).filter(
                Product.price >= min_price,
                Product.price <= max_price
            ).all()
            return products
        finally:
            session.close()
    
    def get_users_with_order_count(self) -> list:
        """Get users with their order counts"""
        session = self.get_session()
        try:
            result = session.query(
                User,
                func.count(Order.id).label('order_count')
            ).outerjoin(Order).group_by(User.id).all()
            
            users_with_counts = []
            for user, count in result:
                users_with_counts.append({
                    'user': user,
                    'order_count': count
                })
            return users_with_counts
        finally:
            session.close()
    
    def update_user_email(self, user_id: int, new_email: str):
        """Update user email"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.email = new_email
                session.commit()
                print(f"User {user_id} email updated to {new_email}")
            else:
                print(f"User {user_id} not found")
        except Exception as e:
            session.rollback()
            print(f"Error updating user: {e}")
        finally:
            session.close()
    
    def update_product_stock(self, product_id: int, new_stock: int):
        """Update product stock"""
        session = self.get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            if product:
                product.stock = new_stock
                session.commit()
                print(f"Product {product_id} stock updated to {new_stock}")
            else:
                print(f"Product {product_id} not found")
        except Exception as e:
            session.rollback()
            print(f"Error updating product: {e}")
        finally:
            session.close()
    
    def delete_user(self, user_id: int):
        """Delete a user"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                print(f"User {user_id} deleted")
            else:
                print(f"User {user_id} not found")
        except Exception as e:
            session.rollback()
            print(f"Error deleting user: {e}")
        finally:
            session.close()
    
    def get_statistics(self) -> dict:
        """Get database statistics"""
        session = self.get_session()
        try:
            user_count = session.query(func.count(User.id)).scalar()
            product_count = session.query(func.count(Product.id)).scalar()
            order_count = session.query(func.count(Order.id)).scalar()
            avg_product_price = session.query(func.avg(Product.price)).scalar()
            total_order_quantity = session.query(func.sum(Order.quantity)).scalar()
            
            return {
                'user_count': user_count,
                'product_count': product_count,
                'order_count': order_count,
                'avg_product_price': round(avg_product_price, 2) if avg_product_price else 0,
                'total_order_quantity': total_order_quantity or 0
            }
        finally:
            session.close()
    
    def complex_query_example(self):
        """Demonstrate complex query with joins and filtering"""
        session = self.get_session()
        try:
            # Get users who have ordered products in a specific price range
            result = session.query(User).join(Order).join(Product).filter(
                Product.price >= 100,
                Product.price <= 500
            ).distinct().all()
            
            return result
        finally:
            session.close()


def main():
    """Main function to demonstrate SQLAlchemy operations"""
    db_path = "sqlalchemy_example.db"
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("SQLAlchemy ORM Example")
    print("=" * 50)
    
    # Initialize database manager
    db = DatabaseManager(db_path)
    
    # Create tables
    print("\n1. Creating database tables:")
    db.create_tables()
    
    # Add sample data
    print("\n2. Adding sample data:")
    user1 = db.add_user("Alice Johnson", "alice@example.com", 28)
    user2 = db.add_user("Bob Smith", "bob@example.com", 35)
    user3 = db.add_user("Charlie Brown", "charlie@example.com", 42)
    
    product1 = db.add_product("Laptop", 999.99, "Electronics", 50)
    product2 = db.add_product("Mouse", 29.99, "Electronics", 200)
    product3 = db.add_product("Desk Chair", 199.99, "Furniture", 30)
    product4 = db.add_product("Monitor", 299.99, "Electronics", 40)
    
    # Add orders
    print("\n3. Adding orders:")
    db.add_order(user1.id, product1.id, 1)
    db.add_order(user1.id, product2.id, 2)
    db.add_order(user2.id, product1.id, 1)
    db.add_order(user3.id, product3.id, 3)
    db.add_order(user1.id, product4.id, 2)
    
    # Query data
    print("\n4. Querying data:")
    print("All users:")
    for user in db.get_all_users():
        print(f"  {user}")
    
    print(f"\nUser by ID {user1.id}:")
    print(f"  {db.get_user_by_id(user1.id)}")
    
    print(f"\nUser by email:")
    print(f"  {db.get_user_by_email('bob@example.com')}")
    
    # Filter products
    print("\n5. Filtering products:")
    print("Electronics products:")
    for product in db.get_products_by_category("Electronics"):
        print(f"  {product.name}: ${product.price}")
    
    print("\nProducts in price range $100-$500:")
    for product in db.get_products_in_price_range(100, 500):
        print(f"  {product.name}: ${product.price}")
    
    # Users with order counts
    print("\n6. Users with order counts:")
    for item in db.get_users_with_order_count():
        user = item['user']
        count = item['order_count']
        print(f"  {user.name}: {count} orders")
    
    # Update data
    print("\n7. Updating data:")
    db.update_user_email(user1.id, "alice.new@example.com")
    db.update_product_stock(product2.id, 150)
    
    # Complex query
    print("\n8. Complex query (users with orders $100-$500):")
    for user in db.complex_query_example():
        print(f"  {user.name}")
    
    # Statistics
    print("\n9. Database statistics:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Cleanup
    print("\n10. Cleanup:")
    db.drop_tables()
    os.remove(db_path)
    print("Database cleanup completed.")


if __name__ == "__main__":
    main()