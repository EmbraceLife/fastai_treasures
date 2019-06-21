from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

###############################################################################
###############################################################################
t = [1,2,4]
hasattr(t, "__radd__")
del L.__radd__
t = L(1,2,3)
hasattr(t, "__radd__")
###############################################################################
@patch
def __radd__(a:L,b):
    """
    why L.__radd__
    - we can add b to the end of a, using `L(a)+b`
    - but can we do `b + L(a)` and add `b` to the front of `a`?

    how to use L.__radd__
    - just do `b + L(a)`
    """
    return L(b)+a
###############################################################################
t = L(1,2,3)
hasattr(t, "__radd__")
t.__radd__(4)
5 + t
t
