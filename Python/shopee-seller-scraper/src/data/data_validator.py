# Module for binary search and sorting
from bisect import bisect_left

# Binary search algorithm
def BinSearch(a, x):
    elem = bisect_left(a, x)
    if elem != len(a) and a[elem] == x:
        return True
    else:
        return False