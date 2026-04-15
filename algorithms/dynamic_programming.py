"""
Advanced Algorithms - Dynamic Programming Examples
"""

from functools import lru_cache
from typing import List


def fibonacci_recursive(n: int) -> int:
    """Naive recursive Fibonacci - O(2^n)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """Memoized Fibonacci - O(n)"""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def fibonacci_dp(n: int) -> int:
    """Dynamic Programming Fibonacci - O(n) space O(1)"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def fibonacci_dp_array(n: int) -> int:
    """Dynamic Programming Fibonacci with array - O(n) space O(n)"""
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack Problem - Dynamic Programming
    Each item can be used at most once
    """
    n = len(weights)
    
    # Create DP table
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill the DP table
    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]


def knapsack_unbounded(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Unbounded Knapsack Problem - Dynamic Programming
    Each item can be used unlimited times
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for w in range(capacity + 1):
        for i in range(n):
            if weights[i] <= w:
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    
    return dp[capacity]


def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Longest Common Subsequence - Dynamic Programming
    Find the length of the longest subsequence common to both strings
    """
    m, n = len(text1), len(text2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def longest_common_subsequence_string(text1: str, text2: str) -> str:
    """
    Longest Common Subsequence - Return the actual subsequence
    """
    m, n = len(text1), len(text2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find the LCS string
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))


def longest_palindromic_subsequence(s: str) -> int:
    """
    Longest Palindromic Subsequence - Dynamic Programming
    Find the length of the longest subsequence that is a palindrome
    """
    n = len(s)
    
    # Create DP table
    dp = [[0] * n for _ in range(n)]
    
    # Every single character is a palindrome of length 1
    for i in range(n):
        dp[i][i] = 1
    
    # Fill the DP table
    for cl in range(2, n + 1):  # cl = current length
        for i in range(n - cl + 1):
            j = i + cl - 1
            if s[i] == s[j] and cl == 2:
                dp[i][j] = 2
            elif s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i + 1][j])
    
    return dp[0][n - 1]


def coin_change(coins: List[int], amount: int) -> int:
    """
    Coin Change Problem - Dynamic Programming
    Find the minimum number of coins to make up the amount
    """
    # Initialize DP array with infinity
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0 coins needed to make amount 0
    
    # Fill the DP array
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    Coin Change Problem - Number of ways to make amount
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make amount 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]


def edit_distance(word1: str, word2: str) -> int:
    """
    Edit Distance (Levenshtein Distance) - Dynamic Programming
    Minimum number of operations to convert word1 to word2
    Operations: insert, delete, replace
    """
    m, n = len(word1), len(word2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
    
    return dp[m][n]


def maximum_subarray(nums: List[int]) -> int:
    """
    Maximum Subarray Problem - Kadane's Algorithm
    Find the contiguous subarray with the largest sum
    """
    if not nums:
        return 0
    
    max_sum = current_sum = nums[0]
    
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum


def climbing_stairs(n: int) -> int:
    """
    Climbing Stairs Problem - Dynamic Programming
    Number of distinct ways to climb to the top of n stairs
    You can climb 1 or 2 steps at a time
    """
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def climbing_stairs_optimized(n: int) -> int:
    """
    Climbing Stairs - Space Optimized
    """
    if n <= 2:
        return n
    
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    
    return b


def main():
    """Main function to demonstrate dynamic programming examples"""
    print("Dynamic Programming Examples")
    print("=" * 50)
    
    # Fibonacci examples
    print("\n1. Fibonacci Sequence:")
    n = 10
    print(f"   Recursive: fibonacci_recursive({n}) = {fibonacci_recursive(n)}")
    print(f"   Memoized: fibonacci_memoized({n}) = {fibonacci_memoized(n)}")
    print(f"   DP (space O(1)): fibonacci_dp({n}) = {fibonacci_dp(n)}")
    print(f"   DP (space O(n)): fibonacci_dp_array({n}) = {fibonacci_dp_array(n)}")
    
    # Knapsack problems
    print("\n2. Knapsack Problems:")
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    print(f"   0/1 Knapsack: {knapsack_01(weights, values, capacity)}")
    print(f"   Unbounded Knapsack: {knapsack_unbounded(weights, values, capacity)}")
    
    # Longest Common Subsequence
    print("\n3. Longest Common Subsequence:")
    text1 = "abcde"
    text2 = "ace"
    print(f"   LCS length: {longest_common_subsequence(text1, text2)}")
    print(f"   LCS string: '{longest_common_subsequence_string(text1, text2)}'")
    
    # Longest Palindromic Subsequence
    print("\n4. Longest Palindromic Subsequence:")
    s = "bbbab"
    print(f"   LPS length: {longest_palindromic_subsequence(s)}")
    
    # Coin Change
    print("\n5. Coin Change Problem:")
    coins = [1, 2, 5]
    amount = 11
    print(f"   Minimum coins: {coin_change(coins, amount)}")
    print(f"   Number of ways: {coin_change_ways(coins, amount)}")
    
    # Edit Distance
    print("\n6. Edit Distance:")
    word1 = "horse"
    word2 = "ros"
    print(f"   Edit distance between '{word1}' and '{word2}': {edit_distance(word1, word2)}")
    
    # Maximum Subarray
    print("\n7. Maximum Subarray:")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"   Maximum subarray sum: {maximum_subarray(nums)}")
    
    # Climbing Stairs
    print("\n8. Climbing Stairs:")
    n = 5
    print(f"   Ways to climb {n} stairs: {climbing_stairs(n)}")
    print(f"   Optimized: {climbing_stairs_optimized(n)}")
    
    print("\n" + "=" * 50)
    print("Dynamic Programming Key Concepts:")
    print("✓ Break complex problems into simpler subproblems")
    print("✓ Store solutions to subproblems to avoid redundant computation")
    print("✓ Build up solutions from smaller subproblems")
    print("✓ Optimize space complexity when possible")
    print("✓ Identify overlapping subproblems and optimal substructure")


if __name__ == "__main__":
    main()