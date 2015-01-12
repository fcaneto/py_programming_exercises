"""
Problem statement: https://www.hackerrank.com/contests/quora-haqathon/challenges/archery
"""

def get_quadrant(x, y):
    return (x > 0, y > 0)

N = int(input())
radios = [int(x) for x in input().split()]
M = int(input())
arrows = []
for _ in range(M):
    arrows.append([int(x) for x in input().split()])

radios = sorted(radios)
q_count = 0
for arrow in arrows:
    x1, y1, x2, y2 = arrow[0], arrow[1], arrow[2], arrow[3]
    frontiers = [max(abs(x1), abs(y1)) + 1, max(abs(x2), abs(y2)) + 1]
    frontiers.sort()
    
    #if get_quadrant(x1, y1) != get_quadrant(x2, y2):
        # adjust frontiers to ignore double-crossed radius
        #frontiers[0] = 
    
    for r in radios:
        if r >= frontiers[0]:
            if r < frontiers[1]:
                q_count += 1

print(q_count)