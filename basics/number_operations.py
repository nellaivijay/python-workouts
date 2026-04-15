"""
Python Basics - Number Operations
"""

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci(n):
    """Generate Fibonacci sequence up to n terms"""
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

def factorial(n):
    """Calculate factorial of a number"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def gcd(a, b):
    """Calculate Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate Least Common Multiple"""
    return (a * b) // gcd(a, b)

def main():
    print(f"Is 17 prime? {is_prime(17)}")
    print(f"Fibonacci(10): {fibonacci(10)}")
    print(f"Factorial(5): {factorial(5)}")
    print(f"GCD(48, 18): {gcd(48, 18)}")
    print(f"LCM(48, 18): {lcm(48, 18)}")

if __name__ == "__main__":
    main()