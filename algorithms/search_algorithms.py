"""
Algorithms - Search Algorithms
"""

def linear_search(arr, target):
    """Linear Search - O(n)"""
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1

def binary_search(arr, target):
    """Binary Search - O(log n) - requires sorted array"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def jump_search(arr, target):
    """Jump Search - O(√n) - requires sorted array"""
    n = len(arr)
    step = int(n ** 0.5)
    prev = 0
    
    # Find the block where target may be present
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(n ** 0.5)
        if prev >= n:
            return -1
    
    # Linear search in the identified block
    while arr[prev] < target:
        prev += 1
        if prev == min(step, n):
            return -1
    
    if arr[prev] == target:
        return prev
    return -1

def exponential_search(arr, target):
    """Exponential Search - O(log n) - requires sorted array"""
    if arr[0] == target:
        return 0
    
    i = 1
    n = len(arr)
    
    while i < n and arr[i] <= target:
        i *= 2
    
    return binary_search(arr[:min(i, n)], target)

def main():
    test_array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    targets = [7, 1, 19, 8, 0]
    
    print("Test array:", test_array)
    print("\nSearch Results:")
    
    for target in targets:
        print(f"\nSearching for {target}:")
        print(f"  Linear Search: {linear_search(test_array, target)}")
        print(f"  Binary Search: {binary_search(test_array, target)}")
        print(f"  Jump Search: {jump_search(test_array, target)}")
        print(f"  Exponential Search: {exponential_search(test_array, target)}")

if __name__ == "__main__":
    main()