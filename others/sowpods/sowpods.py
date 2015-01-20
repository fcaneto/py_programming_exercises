import time

def timed_function(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print('> %s took %s seconds' % (f.__name__, end - start))
        return result
    return f_timer

def read_swopods():
    words = []
    with open('sowpods.txt') as f:
        words = [w.strip() for w in f.readlines()]
    return words


@timed_function
def find_longest_palindrome(words):

    def is_palindrome(w):
        i = 0
        j = len(w) - 1

        while i < j:
            if w[i] != w[j]:
                break
            i += 1
            j -= 1

        return i >= j

    lp = None
    for word in words:
        if is_palindrome(word):
            if lp is None or len(word) > len(lp):
                lp = word
    return lp


@timed_function
def find_most_repeated_char(words):

    def find_most_repeated_in_word(w):
        frequencies = {}
        most_repeated = None # tuple (char, frequency)

        for c in w:
            if c not in frequencies:
                frequencies[c] = 1
            else:
                frequencies[c] = frequencies[c] + 1

            if most_repeated is None or frequencies[c] > most_repeated[1]:
                most_repeated = (c, frequencies[c])

        return most_repeated

    all_words_most_repeated = None # tuple (char, frequency, word)
    for word in words:
        char, frequency = find_most_repeated_in_word(word)
        if all_words_most_repeated is None or frequency > all_words_most_repeated[1]:

            all_words_most_repeated = (char, frequency, word)

    return all_words_most_repeated


def get_histogram(w):
    """
    '<char><frequency>' string, sorted by chars,

    ex: bus => b1s1u1
    """
    histogram = {}
    
    for c in w:
        if c not in histogram:
            histogram[c] = 1
        else:
            histogram[c] += 1
    
    key = ''
    for c in sorted(histogram.keys()):
        key += '%s%s' % (c, histogram[c])

    return key


@timed_function
def find_longest_anagram(words):
    histograms = {}

    longest_anagrams = None # tuple 2 words
    
    for w in words:
        key = get_histogram(w)
        if key not in histograms:
            histograms[key] = [w]
        else:
            histograms[key].append(w)
            if longest_anagrams is None or len(w) > len(longest_anagrams[0]):
                longest_anagrams = histograms[key]
    
    return longest_anagrams

from pympler import summary, muppy

if __name__ == "__main__":
    print('SOWPODS analyzer')
    words = read_swopods()
    print('Total: %s words' % len(words))

    print('%s is the longest palindrome' % (find_longest_palindrome(words)))

    char, frequency, word = find_most_repeated_char(words)
    print("'%s' is the most repeated character in one word (in '%s', occurs %s times)" % (char, word, frequency))

    print("%s are the longest anagrams" % (find_longest_anagram(words)))

    all_objects = muppy.get_objects()
    sum1 = summary.summarize(all_objects)
    summary.print_(sum1) 