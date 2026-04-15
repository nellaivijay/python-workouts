"""
Object-Oriented Programming - Class Examples
"""

from abc import ABC, abstractmethod
from typing import List


class Animal:
    """Basic Animal class demonstrating encapsulation"""
    
    def __init__(self, name: str, age: int):
        self.name = name  # Public attribute
        self._age = age  # Protected attribute (convention)
        self.__species = "Unknown"  # Private attribute
    
    def speak(self) -> str:
        """Abstract method to be overridden"""
        return "Some sound"
    
    def eat(self) -> str:
        """Common method for all animals"""
        return f"{self.name} is eating."
    
    def sleep(self) -> str:
        """Common method for all animals"""
        return f"{self.name} is sleeping."
    
    def get_age(self) -> int:
        """Getter for age"""
        return self._age
    
    def set_age(self, age: int):
        """Setter for age with validation"""
        if age > 0:
            self._age = age
        else:
            raise ValueError("Age must be positive")
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.name} ({self.__class__.__name__})"


class Dog(Animal):
    """Dog class inheriting from Animal"""
    
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)
        self.breed = breed
    
    def speak(self) -> str:
        """Override speak method"""
        return "Woof! Woof!"
    
    def fetch(self) -> str:
        """Dog-specific method"""
        return f"{self.name} is fetching the ball!"


class Cat(Animal):
    """Cat class inheriting from Animal"""
    
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age)
        self.color = color
    
    def speak(self) -> str:
        """Override speak method"""
        return "Meow!"
    
    def climb(self) -> str:
        """Cat-specific method"""
        return f"{self.name} is climbing the tree."


class Shape(ABC):
    """Abstract base class for shapes"""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate area - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter - must be implemented by subclasses"""
        pass


class Rectangle(Shape):
    """Rectangle class implementing Shape"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def __str__(self) -> str:
        return f"Rectangle ({self.width}x{self.height})"


class Circle(Shape):
    """Circle class implementing Shape"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius
    
    def __str__(self) -> str:
        return f"Circle (radius={self.radius})"


class BankAccount:
    """BankAccount class demonstrating encapsulation and methods"""
    
    def __init__(self, account_number: str, owner: str, balance: float = 0.0):
        self._account_number = account_number
        self._owner = owner
        self._balance = balance
    
    def deposit(self, amount: float) -> bool:
        """Deposit money into account"""
        if amount > 0:
            self._balance += amount
            print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")
            return True
        return False
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money from account"""
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")
            return True
        print(f"Withdrawal failed. Insufficient funds or invalid amount.")
        return False
    
    def get_balance(self) -> float:
        """Get current balance"""
        return self._balance
    
    def __str__(self) -> str:
        return f"Account {self._account_number} - {self._owner}: ${self._balance:.2f}"


class Student:
    """Student class with class methods and static methods"""
    
    school_name = "Python High School"
    
    def __init__(self, name: str, grade: int):
        self.name = name
        self.grade = grade
        self.grades = []
    
    def add_grade(self, grade: float):
        """Add a grade to the student's record"""
        if 0 <= grade <= 100:
            self.grades.append(grade)
        else:
            raise ValueError("Grade must be between 0 and 100")
    
    def get_average(self) -> float:
        """Calculate average grade"""
        if self.grades:
            return sum(self.grades) / len(self.grades)
        return 0.0
    
    @classmethod
    def change_school(cls, new_school: str):
        """Class method to change school name for all students"""
        cls.school_name = new_school
    
    @staticmethod
    def is_passing_grade(grade: float) -> bool:
        """Static method to check if a grade is passing"""
        return grade >= 60.0
    
    def __str__(self) -> str:
        avg = self.get_average()
        return f"{self.name} (Grade {self.grade}): Average = {avg:.2f}"


class Library:
    """Library class demonstrating composition"""
    
    def __init__(self, name: str):
        self.name = name
        self.books = []
    
    def add_book(self, book):
        """Add a book to the library"""
        self.books.append(book)
        print(f"Added '{book.title}' to {self.name}")
    
    def remove_book(self, book_id: int):
        """Remove a book from the library"""
        self.books = [book for book in self.books if book.id != book_id]
        print(f"Removed book with ID {book_id}")
    
    def find_book_by_title(self, title: str):
        """Find a book by title"""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
    def list_books(self):
        """List all books in the library"""
        print(f"\nBooks in {self.name}:")
        for book in self.books:
            print(f"  {book}")


class Book:
    """Book class to be used with Library"""
    
    def __init__(self, book_id: int, title: str, author: str):
        self.id = book_id
        self.title = title
        self.author = author
    
    def __str__(self) -> str:
        return f"Book {self.id}: '{self.title}' by {self.author}"


def main():
    """Main function to demonstrate OOP concepts"""
    print("Object-Oriented Programming Examples")
    print("=" * 50)
    
    # Inheritance example
    print("\n1. Inheritance:")
    animals = [
        Dog("Buddy", 3, "Golden Retriever"),
        Cat("Whiskers", 2, "Calico")
    ]
    
    for animal in animals:
        print(f"{animal} says: {animal.speak()}")
        print(f"  {animal.eat()}")
        if isinstance(animal, Dog):
            print(f"  {animal.fetch()}")
        elif isinstance(animal, Cat):
            print(f"  {animal.climb()}")
    
    # Abstract base class example
    print("\n2. Abstract Base Classes:")
    shapes = [
        Rectangle(5, 3),
        Circle(2)
    ]
    
    for shape in shapes:
        print(f"{shape}")
        print(f"  Area: {shape.area():.2f}")
        print(f"  Perimeter: {shape.perimeter():.2f}")
    
    # Encapsulation example
    print("\n3. Encapsulation:")
    account = BankAccount("12345", "John Doe", 1000.0)
    print(account)
    account.deposit(500.0)
    account.withdraw(200.0)
    account.withdraw(2000.0)  # Should fail
    
    # Class methods and static methods
    print("\n4. Class Methods and Static Methods:")
    student = Student("Alice", 10)
    student.add_grade(85)
    student.add_grade(92)
    student.add_grade(78)
    print(student)
    print(f"School: {Student.school_name}")
    print(f"Is 85 passing? {Student.is_passing_grade(85)}")
    print(f"Is 55 passing? {Student.is_passing_grade(55)}")
    
    # Composition example
    print("\n5. Composition:")
    library = Library("Central Library")
    library.add_book(Book(1, "Python Programming", "John Smith"))
    library.add_book(Book(2, "Data Science", "Jane Doe"))
    library.add_book(Book(3, "Web Development", "Bob Johnson"))
    library.list_books()
    
    found_book = library.find_book_by_title("Python Programming")
    if found_book:
        print(f"\nFound book: {found_book}")
    
    print("\n" + "=" * 50)
    print("OOP Concepts Demonstrated:")
    print("✓ Inheritance and method overriding")
    print("✓ Abstract base classes")
    print("✓ Encapsulation (getters/setters)")
    print("✓ Class methods and static methods")
    print("✓ Composition")
    print("✓ Special methods (__str__, __init__)")

if __name__ == "__main__":
    main()