from collections import deque
filename = 'winning_at_sports.txt'

def solve(x, y, stressfull):

    m = []
    for _ in range(x + 1):
        m.append([0] * (y + 1))

    m[0][0] = 1
    i, j = 0, 0
    visited = set()

    queue = deque()
    if stressfull:
        queue.append((0, 1))
    else:
        queue.append((1, 0))

    while queue:
        i, j = queue.popleft()
        # print(i,j)
        
        from_left = 0
        if j > 0:
            if stressfull and j >= i: # tie or losing
                from_left = m[i][j-1]
            if not stressfull and j < i: # winning
                from_left = m[i][j-1]
        from_top = 0
        if i > 0:
            if stressfull:
                from_top = m[i-1][j]
            elif i > j: # winning 
                from_top = m[i-1][j]

        if from_top and from_left:
            ways = from_top + from_left
        else:
            ways = from_left if from_left else from_top

        m[i][j] = ways

        go_down = False
        if i < x and (i+1, j) not in visited:
            if stressfull:
                if j == y or i < j:
                    go_down = True
            else:
                go_down = True

        if go_down:
            queue.append((i+1, j))
            visited.add((i+1, j))
            
        go_right = False
        if j < y and (i, j+1) not in visited: 
            if stressfull:
                go_right = True
            else:
                 if i == x or i > (j + 1):
                    go_right = True

        if go_right:
            queue.append((i, j+1))
            visited.add((i, j+1))

    return m[x][y] % 1000000007

if __name__ == "__main__":
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):
            x, y = map(int, input_file.readline().strip().split('-'))

            answer1 = solve(x, y, False)
            answer2 = solve(x, y, True)
        
            print("Case #%s: %s %s" % (i, answer1, answer2))
