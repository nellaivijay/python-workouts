"""
Testing Examples - Unit Testing with unittest
"""

import unittest
from typing import List


def add_numbers(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def is_even(number: int) -> bool:
    """Check if a number is even"""
    return number % 2 == 0


def factorial(n: int) -> int:
    """Calculate factorial of a number"""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


def find_max(numbers: List[int]) -> int:
    """Find the maximum number in a list"""
    if not numbers:
        raise ValueError("List cannot be empty")
    return max(numbers)


def reverse_string(s: str) -> str:
    """Reverse a string"""
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome"""
    s = s.lower().replace(" ", "")
    return s == s[::-1]


class TestMathFunctions(unittest.TestCase):
    """Test cases for mathematical functions"""
    
    def test_add_numbers(self):
        """Test the add_numbers function"""
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(2.5, 3.5), 6.0)
    
    def test_divide_numbers(self):
        """Test the divide_numbers function"""
        self.assertEqual(divide_numbers(10, 2), 5)
        self.assertEqual(divide_numbers(-10, 2), -5)
        self.assertEqual(divide_numbers(10, -2), -5)
        
        # Test division by zero
        with self.assertRaises(ValueError):
            divide_numbers(10, 0)
    
    def test_is_even(self):
        """Test the is_even function"""
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(-4))
        self.assertFalse(is_even(1))
        self.assertFalse(is_even(3))
        self.assertFalse(is_even(-1))
    
    def test_factorial(self):
        """Test the factorial function"""
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)
        
        # Test negative input
        with self.assertRaises(ValueError):
            factorial(-1)


class TestStringFunctions(unittest.TestCase):
    """Test cases for string functions"""
    
    def test_reverse_string(self):
        """Test the reverse_string function"""
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("a"), "a")
        self.assertEqual(reverse_string("123"), "321")
    
    def test_is_palindrome(self):
        """Test the is_palindrome function"""
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertTrue(is_palindrome(""))
        self.assertFalse(is_palindrome("hello"))
        self.assertFalse(is_palindrome("python"))


class TestListFunctions(unittest.TestCase):
    """Test cases for list functions"""
    
    def test_find_max(self):
        """Test the find_max function"""
        self.assertEqual(find_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(find_max([5, 4, 3, 2, 1]), 5)
        self.assertEqual(find_max([-1, -2, -3]), -1)
        self.assertEqual(find_max([10]), 10)
        
        # Test empty list
        with self.assertRaises(ValueError):
            find_max([])


class TestDataStructures(unittest.TestCase):
    """Test cases for data structure operations"""
    
    def test_list_operations(self):
        """Test various list operations"""
        test_list = [1, 2, 3, 4, 5]
        
        # Test list length
        self.assertEqual(len(test_list), 5)
        
        # Test list indexing
        self.assertEqual(test_list[0], 1)
        self.assertEqual(test_list[-1], 5)
        
        # Test list slicing
        self.assertEqual(test_list[1:3], [2, 3])
        self.assertEqual(test_list[:3], [1, 2, 3])
        
        # Test list modification
        test_list.append(6)
        self.assertEqual(len(test_list), 6)
        self.assertIn(6, test_list)
    
    def test_dictionary_operations(self):
        """Test various dictionary operations"""
        test_dict = {'a': 1, 'b': 2, 'c': 3}
        
        # Test dictionary access
        self.assertEqual(test_dict['a'], 1)
        self.assertEqual(test_dict.get('d', 'default'), 'default')
        
        # Test dictionary modification
        test_dict['d'] = 4
        self.assertEqual(test_dict['d'], 4)
        self.assertEqual(len(test_dict), 4)
        
        # Test dictionary methods
        self.assertIn('a', test_dict.keys())
        self.assertIn(1, test_dict.values())
        self.assertIn(('a', 1), test_dict.items())


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_zero_division(self):
        """Test handling of zero division"""
        with self.assertRaises(ValueError):
            divide_numbers(1, 0)
    
    def test_empty_string(self):
        """Test handling of empty strings"""
        self.assertEqual(reverse_string(""), "")
        self.assertTrue(is_palindrome(""))
    
    def test_single_element(self):
        """Test handling of single element collections"""
        self.assertEqual(find_max([42]), 42)
        self.assertEqual(reverse_string("a"), "a")
    
    def test_none_handling(self):
        """Test handling of None values (if applicable)"""
        # This would test functions that should handle None
        pass


def run_tests():
    """Run all tests and display results"""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMathFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestStringFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestListFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestDataStructures))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


def main():
    """Main function to run testing examples"""
    print("Python Testing Examples with unittest")
    print("=" * 70)
    print("\nRunning test suite...")
    print()
    
    success = run_tests()
    
    if success:
        print("\n✓ All tests passed successfully!")
    else:
        print("\n✗ Some tests failed. Please review the output above.")
    
    print("\nTesting Best Practices:")
    print("1. Write testable code with clear inputs and outputs")
    print("2. Test both normal cases and edge cases")
    print("3. Use descriptive test names")
    print("4. Keep tests independent and isolated")
    print("5. Test one thing per test method")
    print("6. Use assertions appropriately")
    print("7. Consider using setUp and tearDown for test setup/cleanup")


if __name__ == "__main__":
    main()