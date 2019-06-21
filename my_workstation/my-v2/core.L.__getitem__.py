from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *
from local.core import _mask2idxs

t = [1,2,3]
t[2]
t[0:2]
test_fail(lambda: t[1,2], contains='not tuple')
del L.__getitem__
t = L(1,2,3)
hasattr(t, '__getitem__')
############################################################################

@patch
def __getitem__(cls:L, idx):
    """
    why need __getitem__?
    - We'd like to access any elements of L by its idx
    - even better, if idx is multiple, create a new L instance

    How to use __getitem__?
    - `L(1,2,3)[idx]`
    - `L(1,2,3)[0]`
    - `L(1,2,3)[1,2]`
    - if `idx` is scalar, return a scalar;
    - if `idx` is multiple, return a L object

    How does it work?
    - if `idx` is scalar, assign `cls.items[idx]` to `res`
    - if `idx` is multiple, make sure all masks turned to idxs
        - and put all selected elements into a list
        - assign the list to `res`
    - if `res` is tuple or list but not L, turn it into L
    - return `res`

    Note:
    - without __getitem__
    - L is still iterable, but
    - can't do anything related with looping
    - nor can access elements with idx
    """
    res = [cls.items[i] for i in _mask2idxs(idx)] if is_iter(idx) else cls.items[idx]

    if isinstance(res,(tuple,list)) and not isinstance(res,L): res = L(res)
    return res


L(1,2,3)[0]
L(1,2,3)[1,2]
L(1)
L(1,2,3,4,5)[True, False, True]
map(str, L(1,2,3))


######## run the following block to experiment: what if ############

@patch
def __getitem__(cls:L, idx):
    """
    what if: return None?
    - no error, but only return None
    """
    return None

c = L(1,2,3)
c[0]
c[1,2]
map(str, c)
list(map(str, c))
c

######## run the following block to experiment: what if ############
# if you delete this method,
# L is still iterable, but no more subscriptable
# L can no more access element, nor do looping anymore
del L.__getitem__

c = L(1,2,3)
is_iter(c)
test_fail(lambda: c[0], contains='not subscriptable')
len(c)
map(str, c)
test_fail(lambda: list(map(str, c)),contains='not subscriptable')
g = (i for i in c)
test_fail(lambda: next(g), contains='not subscriptable')
test_fail(lambda:[i for i in c], contains='not subscriptable')
itertools.islice(map(str,c), 10)
test_fail(lambda: ",".join(itertools.islice(map(str,c), 10)), contains='not subscriptable')
test_fail(lambda:c.__repr__(), contains='not subscriptable')
for i in c:
    print(i)
