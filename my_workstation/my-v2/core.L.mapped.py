from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


###############################################################################
###############################################################################
list(map(str, [1,2,3]))
hasattr([1,2,3], 'mapped')
list(map(str, L(1,2,3)))
del L.mapped
hasattr(L, 'mapped')
###############################################################################
@patch
def mapped(cls:L, f):
    """
    why L.mapped(f)?
    - although we can do `list(map(str, L(1,2,3)))` alike
    - we want something simpler and cleaner
    - why not `t.mapped(f)` and return a new L

    how to use L.mapped(f)
    - `t.mapped(str)`
    """
    return L(map(f, cls))
###############################################################################
t = L(1,2,3)
t.mapped(str)
