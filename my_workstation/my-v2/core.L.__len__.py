from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *



@patch
def __len__(cls:L):
    """
    why __len__?
    - we want `len(L(1))` to tell us the total number of items

    how to use __len__?
    - `len(L(1,2,3))`
    """
    return len(cls.items)
################################################################################
# we have to write L.__len__ in order to do `len(t)`
t = L(1,2,3)
len(t)
t.__len__()
