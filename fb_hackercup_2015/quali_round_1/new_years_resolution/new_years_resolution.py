filename = 'in'

import sys
from collections import namedtuple

def is_bigger(t1, t2):
    for e1, e2 in zip(t1, t2):
        if e1 > e2:
            return True
    return False

def is_equals(t1, t2):
    for e1, e2 in zip(t1, t2):
        if e1 != e2:
            return False
    return True

def i_sum(t1, t2):
    s = []
    for e1, e2 in zip(t1, t2):
        s.append(e1 + e2)
    return s

def find_sum(exact_sum, all_foods, candidate_sum, current_start):
    for i in range(current_start, len(all_foods)):
        new_candidate = i_sum(candidate_sum, all_foods[i])
        if is_equals(new_candidate, exact_sum):
            return True

        if not is_bigger(new_candidate, exact_sum):
            next_step = find_sum(exact_sum, all_foods, new_candidate, i)
            if next_step:
                return True

    return False

def solve():
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):
            all_foods = []
            exact_sum = input_file.readline().strip().split()
            exact_sum = list(map(int, exact_sum))

            n = int(input_file.readline().strip())
            for _ in range(n):
                food = input_file.readline().strip().split()
                food =  list(map(int, food))
                if not is_bigger(food, exact_sum):
                    all_foods.append(food)

            found_sum = False
            for j in range(len(all_foods)):
                found_sum = find_sum(exact_sum, all_foods, [0, 0, 0], j)
                if found_sum:
                    break

            answer = 'yes' if found_sum else 'no'
            print("Case #%s: %s" % (i, answer))

solve()

# loop two lists
# sort by several parameters