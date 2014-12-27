"""
Source: Facebook Hackaton page
https://www.facebook.com/hackathon/posts/10152380871190988

When typing in a touch screen "Hello", a "G" might be registered instead of "H".
Write a function that given a string, returns all nearby words.

You have the functions:
- get_nearby_chars: given a char returns a set of nearby chars.
- is_word: given a word, returns if it's valid
"""

def nearby_words(word, limit=100):
    """
    Clarifying questions I thought:
    - get_nearby_chars returns the same char everytime?
    - limit the search space? assuming that can add a limit parameter 
    - how many nearby_chars are returned? assuming only direct neighboors
    - avoid repetitions in the output? 

    Video also proposes:
    - format of word parameter?
    - how do we define a nearby word?
    - does the output has to be sorted?

    Solution:
    - go BFS in the alternatives graph of valid words, editing one char at a time
    """
    solution = set()
    if is_word(word):
        solution.add(word)
        limit -= 1

    alternative_queue = [word]

    while limit > 0 and alternative_queue:
        current_word = alternative_queue.pop(0)

        for index, char in enumerate(current_word):
            for new_char in get_nearby_chars(char):
                if new_char != char:
                    new_word = current_word[:index] + new_char + current_word[index+1:]
                    if is_word(new_word):
                        alternative_queue.append(new_word)
                        if limit > 0:
                            solution.add(new_word)
                            limit -= 1
                        else: 
                            break

    return solution


"""
How to test it?
=> edge cases: empty word, one char word
=> do not include the same string repetition on answer
=> no valid words on permutations of level 1
=> no valid words on permutations of sub-level

Complexity Analysis: n letters, constant nearby letter each
for only one edit on word: O(c ^ n)
"""

def get_nearby_chars(char):
    if char == 'a':
        return ['s', 'z', 'q']
    if char == 'b':
        return ['v', 'g', 'h', 'n']
    return []

def is_word(word):
    return True

print(nearby_words(word='abc'))



