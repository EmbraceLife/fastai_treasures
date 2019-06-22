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
    - add onto module means you can directly access the class, see example below
    """
    stk = inspect.stack()[1]
    mod = ifnone(inspect.getmodule(stk[0]), sys.modules['__main__'])
    res = get_class(nm, *fld_names, sup=sup, doc=doc, funcs=funcs, **flds)
    setattr(mod, nm, res)


############################################
# Any kwargs will be added as class attributes, and sup is an optional (tuple of) base classes.
mk_class('_T', a=10, sup=GetAttr)
_T
t1 = _T() # __init__ without any *args or **kwargs
t1
t1.a
assert(isinstance(t1,GetAttr))
module(t1)
module(_T)
################ reminder of `get_class()` content
# A __init__ is provided that sets attrs for any kwargs,
# and for any args (matching by position to fields),
# along with a __repr__ which prints all attrs.
# The docstring is set to doc.
# You can pass funcs which will be added as attrs with the function names.

def foo(self): return 1
mk_class('_t', 'a', sup=GetAttr, doc='test doc', funcs=foo)
t = _t(3, b=2, _xtra=['lower'], default="GDP") # __init__ with args and kwargs
t.a
t.b
t.lower()
t.foo()
t.__doc__
