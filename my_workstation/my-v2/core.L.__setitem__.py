from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *
from local.core import _listify

###############################################################################
t = [1,2,4]
hasattr(t, "__setitem__")
t[2] = 3; t
# t[0:2] = 10 # fail because 10 is not iterable
t[0:2] = [10, 10]; t
# t[1,0] = 9
test_fail(lambda: t.__setitem__([0,1], 9), contains="not list")

del L.__setitem__
t = L(1,2,3)
hasattr(t, "__setitem__")
###############################################################################

@patch
def __setitem__(cls:L, idx, o):
    """
    "Set `idx` (can be list of indices, or mask, or int) items to `o` (which is broadcast if not iterable)"

    why L.__setitem__
    - we must be able to do `t[idx] = value`
    - to be more flexible than list, we need to do
        - t[idx1, idx2] = value
        - t[idx1, idx2] = value1, value2

    how to create L.__setitem__
    - make sure `idx` is a L or [...]
    - make sure `o` is iterable or [o, o, o, ...] matching `len(idx)`
    - use `list.__setitem__` to set the value for each item
    """
    idx = idx if isinstance(idx,L) else _listify(idx)
    if not is_iter(o): o = [o]*len(idx)
    for i,o_ in zip(idx,o): cls.items[i] = o_
###############################################################################
t = L(1,2,3)
t.__setitem__([1,2], 9); t
t[0,1] = 10; t
t.__setitem__((1,0), (9,'9')); t
t.items
t # same? not at all, they all turned into string by coll_repr
