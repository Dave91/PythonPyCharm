import random
import time
import bisect  # useful import in this topic


def norm_search(seq, val):
    for l1 in seq:
        if l1 == val:
            print("found")
            return
    print("search over, not found")


def binary_search(sequence, item):
    left_ind = 0
    right_ind = len(sequence) - 1
    while left_ind <= right_ind:
        mid_ind = left_ind + (right_ind - left_ind) // 2
        mid_val = sequence[mid_ind]
        if mid_val == item:
            print("found")
            return mid_ind
        elif item < mid_val:
            right_ind = mid_ind - 1
        else:
            left_ind = mid_ind + 1
    print("search over, not found")
    return None


src_list = [n for n in range(100000000)]
target = 88910000

start1 = time.perf_counter()
norm_search(src_list, target)
end1 = time.perf_counter()
print(end1 - start1)

start2 = time.perf_counter()
binary_search(src_list, target)
end2 = time.perf_counter()
print(end2 - start2)
