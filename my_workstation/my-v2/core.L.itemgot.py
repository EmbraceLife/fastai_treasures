from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


###############################################################################
###############################################################################
@patch
def itemgot(cls:L, idx):
    """
    why L.itemgot(idx)
    - if L object `t` contains multiple lists and we want to access the third item of all the lists
    - we want `t.itemgot(2)` to get the result we wanted
    - list has no such method

    how to create L.itemgot(idx)
    - `itemgetter(2)` is to get the third value
    - `L.mapped()` apply to every item in `t`

    Note:
    - t must have mutiple iterable objects inside, which share the same length
    """
    return cls.mapped(itemgetter(idx))
###############################################################################
t = L([[1,2,3],[4,5,6]]); t
t.itemgot(1)
t = L([tensor(1,2,3), tensor(4,5,6)]); t
t.itemgot(2)
