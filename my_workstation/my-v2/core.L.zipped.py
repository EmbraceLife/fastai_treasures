from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

###############################################################################
###############################################################################
z = zip([1,2,3], ['a','b', 'c']); z
set(z)
L(z)
# L and zip don't work well
t = L([[1,2,3], ['a','b', 'c']]); t
list(zip(t))
###############################################################################
@patch
def zipped(cls:L):
    """
    why L.zipped()?
    - we want to zip to work directly on L just like zip on list
    - but as you can see above `list(zip(t))` won't work on L
    - why not make it work with simpler and cleaner form

    how to use L.zipped()
    - watch out for what is inside `t`
    - `t = L([[1,2,3], ['a', 'b', 'c']])`
    - `t.zipped()`
    """
    return L(zip(*cls))
###############################################################################
t = L([[1,2,3],'abc']); t
t.zipped()
t = L([[1,2,3], ['a', 'b', 'c']]); t
t.zipped()
