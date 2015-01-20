"""
Given an array with arbitrary integers, find the biggest sum formed by contiguous elements.

Solution: Kadane's algorithm, O(n) time complexity

>>> max_subarray_sum([0])
0, (0, 0)
>>> max_subarray_sum([3, -2, 1, 2, -2])
4, (0, 3)
>>> max_subarray_sum([-1, 1, -1, 3, -1 -2, 2])
3, (3, 3)

"""
def max_subarray_sum(array):
    candidate_sum = 0
    
    current_sum = 0
    current_sum_start = 0

    candidate_start = 0
    candidate_end = 0

    for i, n in enumerate(array):
        current_sum = n + current_sum
        
        if current_sum > candidate_sum:
            candidate_sum = current_sum
            candidate_start = current_sum_start
            candidate_end = i

        if current_sum <= 0:
            current_sum = 0
            candidate_sum_start = i + 1

    return candidate_sum, (candidate_start, candidate_end)




