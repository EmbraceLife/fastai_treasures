from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

def coll_repr(c, max=1000):
    """
    purpose:
    1. how to print out the large collection of data?
    2. we want to see its length, and the first ten items of them
    """
    return f'(#{len(c)}) [' + ','.join(itertools.islice(map(str,c), 10)) + ('...'
            if len(c)>10 else '') + ']'

show_doc(itertools.islice)
show_doc(map)
is_iter(t)
t = L(1,2,3,4,5,6,7,8,9,10,11); t
m = map(str, t); m
is_iter(m)
m_iter = itertools.islice(m, 5); m_iter
list(m_iter)
f'.'.join(m_iter)
# pdb
coll_repr(range(1000))
coll_repr(range(9))
coll_repr(torch.tensor([[1,2],[3,4]]), max=1000)
# notebook
test_eq(coll_repr(range(1000)), '(#1000) [0,1,2,3,4,5,6,7,8,9...]')
c = range(1000)
list(itertools.islice(map(str,c), 10))
c = torch.tensor([[1,2],[3,4]])
list(itertools.islice(map(str,c), 10))
