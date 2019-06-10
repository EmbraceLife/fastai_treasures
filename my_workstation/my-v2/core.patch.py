from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

import copy

def patch(f):
    """
    "Decorator: add `f` to the first parameter's class (based on f's type annotations)"

    purpose:
    1. add another method to an existing class
        needs going back to class source and add a method
    2. life would be much easier to write a method/func anywhere and
        it will automatically add itself to a class
    3. we want such a feature be ready for any class to add methods

    steps:
    1. get the class info from func's annotations
    2. wrap `f` with its own copy `nf`
    3. set up `nf.__qualname__` by f"{cls.__name__}.{f.__name__}"
    4. setattr(cls, f.__name__, nf)
    5. return the `f`
    """
    cls = next(iter(f.__annotations__.values()))
    nf = copy.copy(f)
    functools.update_wrapper(nf,f)
    nf.__qualname__ = f"{cls.__name__}.{f.__name__}"
    setattr(cls, f.__name__, nf)
    return f

########################
# a simple class with only __init__ method
class _T2():
    def __init__(self, o): self.foo = getattr(o,'foo',0) + 1

#######################
# a simple decorator @patch can make life easier
@patch
def func(x:_T2, a:bool):
    "test"
    return a+2

t = _T2(1)
t.__init__
t.func


#######################
# decorator made_uncool
def func(x:_T2, a:bool):
    "test"
    return a+2
func = patch(func)

t = _T2(1) # create a _T2 instance, t
test_eq(t.func(1), 3) # this t has a method func
test_eq(t.func.__qualname__, '_T2.func')
