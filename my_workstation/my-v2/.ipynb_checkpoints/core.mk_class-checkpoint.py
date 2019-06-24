from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import *

show_doc(mk_class)# check latest source and test

def mk_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    """
    "Create a class using `get_class` and add to the caller's module"

    why mk_class(...)
    - `get_class(...)` can create a new class with specified attrs for us
    - but what if we want to add this class onto the caller's module
    - we use `mk_class` to create and add onto module altogether

    how to use mk_class(...)
    - the same as get_class(...)
    - but does not return anything

    Note:
    - get_class(...) returns a new class
    - new class is added onto local.core
    - for some reason, `t.__repr__` won't work  
    - so, just use `wrap_class` or `get_class`, not `mk_class`
    """
    def mk_class(nm, *fld_names, sup=None, doc=None, funcs=None, mod=None, **flds):
        "Create a class using `get_class` and add to the caller's module"
        if mod is None: mod = inspect.currentframe().f_back.f_locals
        res = get_class(nm, *fld_names, sup=sup, doc=doc, funcs=funcs, **flds)
        mod[nm] = res

# Caution: run this func at __main__, will disable itself, so run the following 
# two lines to restore the official func
del mk_class
from local.core import *

def foo(self): return 1
mk_class('_t', 'a', sup=GetAttr, doc='test doc', funcs=foo)
t = _t(3, b=2, _xtra=['lower'], default="GDP");t # __init__ 

# t. tab to see all attributes