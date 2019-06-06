from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import patch


#######################
# noop(x=None, *args, **kwargs) => do nothing to `x`, just return it

def noop (x=None, *args, **kwargs):
    "Do nothing"
    return x

def examples():
    noop()
    test_eq(noop(1),1)


########################
# noops(self, x, *args, **kwargs) => do nothing
    # = to be a method of any class, since it uses `self`

def noops(self, x, *args, **kwargs):
    "Do nothing (method)"
    return x

def examples():
    class _t(): foo=noops
    test_eq(_t().foo(1),1)
