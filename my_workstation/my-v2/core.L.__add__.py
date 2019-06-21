from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *
from local.core import _listify





###############################################################################
###############################################################################
t = [1,2,4]
hasattr(t, "__add__")
t.__add__([5])
t = L(1,2,3)
hasattr(t, "__add__")

del L.__add__
t = L(1,2,3)
test_fail(lambda: t.__add__(4), contains='__add__')
###############################################################################
@patch
def __add__ (a:L,b):
    """
    why L.__add__?
    - list can add list into a longer list
    - we want it for L, and much more flexible
    - we want L can be added with not just list but anything else

    How to use L.__add__?
    - t.__add__([9])
    - t.__add__(9)
    - t.__add__(tensor(9))
    - t.__add__([tensor(9)])
    - t.__add__(range(9))
    - t + 10

    How to create L.__add__
    - turn `b` into a list or [] by `_listify(b)`
    - do list.__add__ with a.items
    - turn it into L
    """
    return L(a.items+_listify(b))
###############################################################################
t=L(1,2,3)
hasattr(t, "__add__")
t.__add__([9])
t.__add__(9)
t.__add__(tensor(9))
t.__add__([tensor(9)])
t.__add__(range(9))
t + 10
