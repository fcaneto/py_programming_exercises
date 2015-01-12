"""
Problem statement: http://codeforces.com/contest/497/problem/A
""" 

OK = 1
UNKNOWN = 2
BAD = 3

def get_prefix(word, start, end, removed_columns):
    prefix = ""
    for i in range(start, end+1):
        if i not in removed_columns:
            prefix += word[i]
    return prefix

def analyze_column(words, start, end, removed_columns):
    status = GOOD
    current_prefix = get_prefix(word[0], start, end, removed_columns)
    for word in words[1:]:
        if current_prefix > get_prefix(word[index], start, end, removed_columns):
            return BAD
        elif current_char == word[index]:
            status = UNKNOWN
    return status

def remove_columns(n, m, words):
    removed_columns = set()
    prefix_start = 0
    for column in range(m):
        status = analyze_column(words, start=prefix_start, end=column, removed_columns=removed_columns)
        if status == GOOD:
            break
        elif status == BAD:
            removed_columns.add(column)
            if not prefix_start:
                prefix_start += 1

    return len(removed_columns)


n, m = input().split()
words = []
for i in range(n):
    words[i] = input()        

print(remove_columns(n, m, words))




