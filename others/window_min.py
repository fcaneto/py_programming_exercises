"""
Tracks the minimum value within a k-sized window, 
that slides through a (possibly infinite) stream of integers.

Solution: 
- Store the minimum candidates in a deque. At each new element:
    - remove candidates from the head of the deque that aren't on the window anymore.
    - remove candidates from the tail that are bigger than the new element

Using a heap, each new element would incur an O(logk) cost.
This solution gives an amortized O(1) cost.

>>> list(window_min([1, 2, 3], 1))
[1, 2, 3]

>>> list(window_min([10, 9, 8, 10, 11, 15, 12, 13, 7, 16], 3))
[10, 9, 8, 8, 8, 10, 11, 12, 7, 7]

>>> list(window_min([8, 9, 10, 8, 9], 3))
[8, 8, 8, 8, 8]

"""
from collections import namedtuple, deque

Entry = namedtuple('Entry', ['value', 'position'])

def window_min(iterable, k):
    candidates = deque()
    window = deque()

    counter = 0    
    for n in iterable:

        if counter < k:
            window_position = 0  
        else: 
            window_position = counter - k + 1
        
        # remove old minimums from head
        if candidates:
            head = candidates[0]
            while head.position < window_position and candidates:
                candidates.popleft()
                if candidates:
                    head = candidates[0]

        # removing non-candidates from tail
        if candidates:
            last = candidates[-1]
            while last.value > n and candidates:
                candidates.pop()
                if candidates:
                    last = candidates[-1]

        candidates.append(Entry(value=n, position=counter))
        counter += 1

        yield candidates[0].value

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    

