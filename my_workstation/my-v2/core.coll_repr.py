from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

show_doc(coll_repr)

def coll_repr(c, max=10):
    """
    why `coll_repr`? because
    - we want to print out a representation of a collection of things
    - a good view of the whole thing but not too long

    how to use `coll_repr`?
    - `coll_repr(c, max=1000)`
    - `c`: the collection, like L
    - `max`: the number of items you want to print out

    how `coll_repr` work?
    - first, make each element of the collection a string
    - second, slice `max` number of elements from `c` into an iterator
    - third, bind each sliced element with ','
    - the rest string is easier to understand
    """
    return f'(#{len(c)}) [' + ','.join(itertools.islice(map(str,c), max)) + ('...'
            if len(c)>max else '') + ']'

# to experiment with the itertools.islice
g = itertools.islice(map(str,c), max)
next(g)
# simple examples
coll_repr(c=L(range(100,110)), max=5)
coll_repr(range(1000))
coll_repr(range(9))
coll_repr(torch.tensor([[1,2],[3,4]]), max=1000)
