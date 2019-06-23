from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import *

show_doc(wrap_class)
###############################################################################
def wrap_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    """
    why wrap_class(...):
    - we have `get_class(...)` to create a new class with specified attrs
    - we have `mk_class(...)` to create and add new class onto caller's module
    - we have `@patch` to add a new method to a class anywhere in an experiment
    - why not have @wrap_class to create, add onto module and create a method whenever and wherever we like very super fast?

    how to use wrap_class(...)?
    - `@wrap_class(...)`: as if we are using `mk_class(...)`
    - immediately create a method as if we were writing a class and its methods

    how to create wrap_class(...)?
    - making a decorator to wrap a method with `mk_class(...)`
    """
    def _inner(f):
        mk_class(nm, *fld_names, sup=sup, doc=doc, funcs=L(funcs)+f, **flds)
        return f
    return _inner

# how to create a class and a method in two lines of code
# def bar1(x): return x+1
@wrap_class('_P', a=2,) # say you want a class called '_t' with attr 'a=2'
def bar(self,x): return x+1 # say you want this class has a method `bar`

t = _P(b='new attr', c=int); t # yeah, __init__ can add additional attrs too
_P
isinstance(t.bar, types.MethodType)
# isinstance(t.bar1, types.MethodType)
