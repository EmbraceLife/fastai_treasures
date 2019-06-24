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
    - why not have @wrap_class to create, add onto module and create a method whenever and wherever we like very fast?

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

# Caution: the func above shall not be executed, 
# if you did, please run `del wrap_class` and `from local.core import *` again
# as the `wrap_class` defined in the __main__ won't work properly


def bar1(self, x): return x+2 # add methods before @wrap_class
bar2 = lambda self, x: self.a + x # self is usually added
@wrap_class('_P', 'alpha', a=2, bar1=bar1, bar2=bar2) # add methods in decorator
def bar(self,x): return x+1 # add methods after decorator
t = _P(100, b='new attr', c=int); t # 100 assigned to 'alpha'

