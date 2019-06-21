from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

############### what can list.__mul__ do
t = [1,2,3]
hasattr(t, '__mul__')
t.__mul__(3)
t*3
t1 = [tensor(1,2,3)]*3
t2 = [tensor(1,2,3)]
test_fail(lambda: t1*t2, contains="can't multiply sequence")

################# without L.__mul__, L can't do the same as above
del L.__mul__
t1 = L(tensor(1,2,3))
t2 = L(tensor(1,2,3))
test_fail(lambda: t1*3, contains="unsupported operand type(s) for *: 'L' and 'int'")

###############################################################################
@patch
def __mul__ (a:L,b):
    """
    why L.__mul__
    - what list.__mul__ can do, so should L.__mul__

    how to use L.__mul__
    - t1.__mul__(int)
    - t1*int

    how to create L.__mul__
    - do list.__mul__ as done in `a.items*b`
    - make it a L instance
    """
    return L(a.items*b)
###############################################################################
t = L(1,2,3)
hasattr(t, '__mul__')
# show_doc(t.__mul__)
t.__mul__(3)
t*3
t1 = L(tensor(1,2,3))
t1*3
