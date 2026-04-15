"""
Python Basics - String Manipulation Exercises
"""

def reverse_string(s):
    """Reverse a string"""
    return s[::-1]

def is_palindrome(s):
    """Check if a string is a palindrome"""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def count_vowels(s):
    """Count vowels in a string"""
    vowels = 'aeiou'
    return sum(1 for char in s.lower() if char in vowels)

def capitalize_words(s):
    """Capitalize the first letter of each word"""
    return ' '.join(word.capitalize() for word in s.split())

def remove_duplicates(s):
    """Remove duplicate characters from a string"""
    return ''.join(dict.fromkeys(s))

def main():
    # Test the functions
    test_string = "hello world"
    
    print(f"Original string: {test_string}")
    print(f"Reversed: {reverse_string(test_string)}")
    print(f"Is palindrome: {is_palindrome('racecar')}")
    print(f"Vowel count: {count_vowels(test_string)}")
    print(f"Capitalized: {capitalize_words(test_string)}")
    print(f"Without duplicates: {remove_duplicates('hello')}")

if __name__ == "__main__":
    main()