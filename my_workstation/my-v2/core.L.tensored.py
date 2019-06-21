from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


###############################################################################
###############################################################################
@patch
def tensored(cls:L):
    """
    why need L.tensored()
    - because we want to turn everything inside L into a tensor

    how to use L.tensored()
    - `t.tensored()`

    how to create L.tensored()
    - the key function is `tensor(element)`
    - we use `L.mapped(f)` to apply to every element

    # NOTE:
    - returns L, not pure tensor
    """
    return cls.mapped(tensor)
###############################################################################
t=L(1,2,3)
t.tensored()
t=L([[1,2,3],])
t.tensored()
