from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


t1 = [1,2,3]
t2 = [1,2,3]
hasattr(t1, '__eq__')
t1.__eq__(t2)
t1.__eq__([1,1,3])

###############################################################################
@patch
def __eq__(cls:L,b):
    """
    why L.__eq__
    - L should at least have `L.__eq__` just like `list.__eq__` above
    - but more flexible and powerful, should be able to compare list of any type
    - so we combine `equals` and `all_equal` to compare list of all types

    how to use `L.__eq__`
    - `t1.__eq__(t2)`

    how to create L.__eq__
    - use `all_equal` to compare all types of items in L
    """
    return all_equal(b,cls)
###############################################################################
hasattr(L, '__eq__')

t1 = L(tensor(1,2,3))
t2 = L(tensor(1,2,3))
t1.__eq__(t2)
