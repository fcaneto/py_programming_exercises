filename = 'in'

def solve():
    pass

if __name__ == "__main__":
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):

            answer = solve()
        
            print("Case #%s: %s" % (i, answer))