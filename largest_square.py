from collections import namedtuple
from operator import mul, sub

try:
    reduce = reduce
except NameError:
    from functools import reduce # py3k

Info = namedtuple('Info', 'start height')

def max_size(mat, value=0):
    """Find height, width of the largest rectangle containing all `value`'s.

    For each row solve "Largest Rectangle in a Histrogram" problem [1]:

    [1]: http://blog.csdn.net/arbuckle/archive/2006/05/06/710988.aspx
    """
    it = iter(mat)
    hist = [int(el==value) for el in next(it, [])]
    (max_y, max_x), max_size = max_rectangle_size(hist)
    for i, row in enumerate(it):
        hist = [(1+h) if el == value else 0 for h, el in zip(hist, row)]
        (new_y, new_x), new_max_size = max_rectangle_size(hist)
        if reduce(mul, new_max_size) > reduce(mul, max_size):
            max_y = (i + 2) - new_y
            max_x = new_x
            max_size = new_max_size
    return (max_y, max_x), max_size

def max_rectangle_size(histogram):
    """Find height, width of the largest rectangle that fits entirely under
    the histogram.

    >>> f = max_rectangle_size
    >>> f([5,3,1])
    (3, 2)
    >>> f([1,3,5])
    (3, 2)
    >>> f([3,1,5])
    (5, 1)
    >>> f([4,8,3,2,0])
    (3, 3)
    >>> f([4,8,3,1,1,0])
    (3, 3)
    >>> f([1,2,1])
    (1, 3)

    Algorithm is "Linear search using a stack of incomplete subproblems" [1].

    [1]: http://blog.csdn.net/arbuckle/archive/2006/05/06/710988.aspx
    """
    stack = []
    top = lambda: stack[-1]
    max_size = (0, 0) # height, width of the largest rectangle
    max_x = 0
    max_y = 0
    pos = 0 # current position in the histogram
    for pos, height in enumerate(histogram):
        start = pos # position where rectangle starts
        while True:
            if not stack or height > top().height:
                stack.append(Info(start, height)) # push
            elif stack and height < top().height:
                max_size, max_x, max_y = max((max_size, max_x, max_y), 
                    ((top().height, (pos - top().start)), top().start, top().height),
                    key=area)
                start, _ = stack.pop()
                continue
            break # height == top().height goes here

    pos += 1
    for start, height in stack:
        max_size, max_x, max_y = max((max_size, max_x, max_y), ((height, (pos - start)), start, height), key=area)


    return (max_y, max_x), max_size

def area(size):
    # Maybe add a term that prefers areas in the middle of the image?
    return reduce(mul, size[0]) / (abs(reduce(sub, size[0])) + 1)**1.5

