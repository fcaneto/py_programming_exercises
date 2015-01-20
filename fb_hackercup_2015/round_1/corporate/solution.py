from collections import deque
from itertools import count

filename = 'corporate_gifting.txt'

def Node(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.children = []


def solve(tree):
    """
    Cases:
    - CEO alone
    - max flat hierarchy
    - max vertical hierarchy
    """
    
    gifts = {}
    queue = deque()
    stack = deque() # simulates recursion

    queue.append(1) # BFS going down

    while queue:
        employee = queue.pop()
        num_children = len(tree[employee])

        if num_children == 0:
            gifts[employee] = 1
        else:
            stack.append(employee)

        for child in tree[employee]:
            queue.append(child)

    # print(gifts)

    while stack:
        # print(stack)
        manager = stack.pop()
        # print(manager)
        subtree = 0
        subtree_values = set()

        values_by_subordinate = {}

        for child in tree[manager]:
            values_by_subordinate[child] = gifts[child]
            subtree_values.add(gifts[child])
            subtree += gifts[child]
        # print('subtree ', subtree, ' - ', subtree_values)
        # print('subs', values_by_subordinate)

        # if there are children with $1 AND $2, try to optimize the more expensive
        if 1 in subtree_values and 2 in subtree_values:
            for subordinate, gift in values_by_subordinate.items():
                if gift == 2:
                    if len(tree[subordinate]) == 1:
                        # exchange gifts
                        gifts[subordinate] = 2
                        son = tree[subordinate].pop()
                        gifts[son] = 1

            # run subtree again
            subtree = 0
            subtree_values = set()
            for child in tree[manager]:
                subtree_values.add(gifts[child])
                subtree += gifts[child]
            # print('subtree optimized', subtree, ' - ', subtree_values)

        for i in count(1):
            if i not in subtree_values:
                gifts[manager] = i
                break

    # print(gifts)
    v = 0
    for gift in gifts.values():
        v += gift
    return v


if __name__ == "__main__":
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):

            N = int(input_file.readline().strip())
            hierarchy = map(int, input_file.readline().strip().split())

            # build adjacency list
            tree = {}
            for j in range(1, N + 1):
                tree[j] = set()

            for j, manager in enumerate(hierarchy):
                if manager != 0:
                    tree[manager].add(j + 1)

            answer = solve(tree)
        
            print("Case #%s: %s" % (i, answer))