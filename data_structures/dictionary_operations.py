"""
Data Structures - Dictionary Operations
"""

def invert_dictionary(d):
    """Invert a dictionary (swap keys and values)"""
    return {value: key for key, value in d.items()}

def sort_dictionary_by_value(d, reverse=False):
    """Sort dictionary by value"""
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))

def merge_dictionaries(dict1, dict2):
    """Merge two dictionaries"""
    result = dict1.copy()
    result.update(dict2)
    return result

def count_word_frequency(text):
    """Count frequency of each word in a text"""
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

def find_most_common(d):
    """Find the key with the highest value"""
    return max(d.items(), key=lambda item: item[1])

def filter_dictionary(d, condition):
    """Filter dictionary based on a condition function"""
    return {key: value for key, value in d.items() if condition(key, value)}

def main():
    # Test dictionary operations
    sample_dict = {'a': 3, 'b': 1, 'c': 2, 'd': 4}
    
    print(f"Original dictionary: {sample_dict}")
    print(f"Inverted: {invert_dictionary(sample_dict)}")
    print(f"Sorted by value: {sort_dictionary_by_value(sample_dict)}")
    
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    print(f"Merged: {merge_dictionaries(dict1, dict2)}")
    
    text = "hello world hello python world python python"
    print(f"Word frequency: {count_word_frequency(text)}")
    print(f"Most common word: {find_most_common(count_word_frequency(text))}")
    
    # Filter example
    print(f"Filtered (values > 2): {filter_dictionary(sample_dict, lambda k, v: v > 2)}")

if __name__ == "__main__":
    main()