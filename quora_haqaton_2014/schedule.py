"""
Problem statement: https://www.hackerrank.com/contests/quora-haqathon/challenges/schedule
"""
n = int(input())
e_time = 0

time_elapsed = 0
prob_to_current_step = 1
tests = []

for _ in range(n):
    test = input().split()
    t, p = int(test[0]), float(test[1])
    tests.append((t, p))

tests.sort(key=lambda x: x[1] * x[0])

for i, test in enumerate(tests):
    t, p = test
    time_elapsed += t
    if i < n-1:
        e_time += time_elapsed * prob_to_current_step * (1 - p)
    else:
        e_time += time_elapsed * prob_to_current_step
    prob_to_current_step = prob_to_current_step * p
    
print(e_time)
    