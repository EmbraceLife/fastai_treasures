from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


@patch
def __delitem__(cls:L, i):
    """
    why need __delitem__:
    - we want to delete an element by its idx

    How to use __delitem__?
    - `L(1,2,3).__delitem__(idx)`

    Watch out:
    - `self.default` and `self.items` share the same reference
    - their values change together
    """
    del(cls.items[i])

# simple examples
t = L(1,2,3)
t.__delitem__(0)
t
t.__delitem__(-1)
t
t.default
t.items
