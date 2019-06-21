from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *



###############################################################################
###############################################################################
t = [1,2,4]
hasattr(t, "__addi__")
del L.__addi__
t = L(1,2,3)
hasattr(t, "__addi__")
###############################################################################
@patch
def __addi__(a:L,b):
    """
    why L.__addi__
    - so that we can do a += b with L objects
    """
    a.items += list(b)
    return a
###############################################################################
t = L(1,2,3)
hasattr(t, "__addi__")
t.__addi__([4])
t
t += [10]
t
