filename = 'in'

def solve():
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):
            
            answer = ''
            print("Case #%s: %s" % (i, answer))

solve()