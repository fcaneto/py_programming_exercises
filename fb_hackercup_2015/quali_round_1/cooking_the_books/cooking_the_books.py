import sys
from collections import namedtuple

class Swap(object):

    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def is_null_swap(self):
        return self.x == self.y

def find_swaps(number, start, current_max_swap, current_min_swap):

    length = len(number)
    if start == length - 1:
        # single digit
        return

    head = number[start]

    for i in range(start+1, length):

        max_swap_candidate = number[current_max_swap.y]
        if number[i] > max_swap_candidate:
            current_max_swap.y = i

        min_swap_candidate = number[current_min_swap.y]
        if number[i] < min_swap_candidate:
            print(min_swap_candidate)
            # zero constraint
            if number[i] != '0' or (number[i] == '0' and start != 0):
                print("> %s %s" % (number[i], start))
                current_min_swap.y = i

    if current_max_swap.is_null_swap or current_min_swap.is_null_swap:
        # keep looking!
        if current_max_swap.is_null_swap:
            current_max_swap.x = current_max_swap.x + 1
            current_max_swap.y = current_max_swap.y + 1
        if current_min_swap.is_null_swap:
            current_min_swap.x = current_min_swap.x + 1
            current_min_swap.y = current_min_swap.y + 1 
        find_swaps(number, start + 1, current_max_swap, current_min_swap)

filename = sys.argv[1]

with open(filename) as input_file:
    t = int(input_file.readline().strip())
    for i in range(1, t + 1):
        n = input_file.readline().strip()

        max_swap = Swap()
        min_swap = Swap()
        find_swaps(n, 0, max_swap, min_swap)

        max_number = n
        min_number = n

        if not max_swap.is_null_swap:
            max_number = n[:max_swap.x] + n[max_swap.y] + n[max_swap.x + 1:max_swap.y] + n[max_swap.x] + n[max_swap.y+1:]
        if not min_swap.is_null_swap:
            min_number = n[:min_swap.x] + n[min_swap.y] + n[min_swap.x + 1:min_swap.y] + n[min_swap.x] + n[min_swap.y+1:]

        print("Case #%s: %s %s" % (i, min_number, max_number))


