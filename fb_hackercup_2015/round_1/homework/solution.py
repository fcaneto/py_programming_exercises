from collections import namedtuple
import math

filename = 'homework.txt'

MAX = 10000000
LIMIT = int(math.sqrt(MAX)) + 1

sieve = [0] * (MAX + 1)
sieve[1] = 1

for i in range(2, LIMIT):
    if sieve[i] > 0:
        continue

    sieve[i] = 1

    num = i + i
    while(num < MAX):
        sieve[num] += 1
        num += i

def solve(a, b, k):
    s = 0
    for i in range(a, b+1):
        if sieve[i] == k:
            s += 1
    return s

if __name__ == "__main__":
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):
            a, b, k = map(int, input_file.readline().strip().split())
            # print(a, b, k)
            print("Case #%s: %s" % (i, solve(a, b, k)))

    