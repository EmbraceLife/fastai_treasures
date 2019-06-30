from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


@patch
def __iter__(cls:L):
    """
    why L.__iter__?
    - with L.__getitem__ we can actually use loop-alike in L
    - but sometimes it is useful to turn L into a generator
    - but we can't use builtin `iter` everywhere,
    - we have to write a custom `__iter__` for L

    how to use it?
    - `g = t.__iter__()`
    - `next(g)`

    how to create __iter__
    - `(self[i] for i in range(len(self)))` is typical way of making generator

    Note:
    - L.__getitem__ is responsible for looping related
    - L.__iter__ is responsible for creating a generator
    """
    return (cls[i] for i in range(len(cls)))


cls = L([1,2,3])
hasattr(cls, '__iter__')
g = cls.__iter__();g
next(g)

