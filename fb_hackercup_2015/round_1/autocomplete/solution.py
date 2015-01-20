filename = 'in'

def add_prefix(word, trie):
    level = trie
    p = []
    reached_leaf = False

    for c in word:
        if c not in level:
            if not reached_leaf:
                p.append(c)
            reached_leaf = True
            level[c] = {}
        else:
            p.append(c)

        level = level[c]

    return p


def solve(words):

    trie = {}
    chars = 0

    for word in words:
        p = add_prefix(word, trie)
        chars += len(p)
    return chars

if __name__ == "__main__":
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):
            n = int(input_file.readline().strip())
            words = []
            for _ in (range(n)):
                words.append(input_file.readline().strip())

            answer = solve(words)
            print("Case #%s: %s" % (i, answer))
