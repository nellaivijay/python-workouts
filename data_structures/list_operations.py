"""
Data Structures - List Operations
"""

def find_second_largest(numbers):
    """Find the second largest number in a list"""
    if len(numbers) < 2:
        return None
    unique_numbers = list(set(numbers))
    unique_numbers.sort()
    return unique_numbers[-2]

def remove_duplicates_list(lst):
    """Remove duplicates from a list while preserving order"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def rotate_list(lst, k):
    """Rotate a list by k positions to the right"""
    if not lst:
        return lst
    k = k % len(lst)
    return lst[-k:] + lst[:-k]

def merge_sorted_lists(list1, list2):
    """Merge two sorted lists into one sorted list"""
    merged = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    merged.extend(list1[i:])
    merged.extend(list2[j:])
    return merged

def find_intersection(list1, list2):
    """Find common elements between two lists"""
    return list(set(list1) & set(list2))

def main():
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    print(f"Original list: {numbers}")
    print(f"Second largest: {find_second_largest(numbers)}")
    print(f"Without duplicates: {remove_duplicates_list(numbers)}")
    print(f"Rotated by 2: {rotate_list(numbers, 2)}")
    
    list1 = [1, 3, 5, 7, 9]
    list2 = [2, 3, 5, 8, 10]
    print(f"Merged sorted: {merge_sorted_lists(list1, list2)}")
    print(f"Intersection: {find_intersection(list1, list2)}")

if __name__ == "__main__":
    main()