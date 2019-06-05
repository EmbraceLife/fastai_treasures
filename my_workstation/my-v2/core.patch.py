from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

import copy

class _T2():
    def __init__(self, o): self.foo = getattr(o,'foo',0) + 1

#######################
# create a decorator to automatically add a function to
# its first parameter Class, when you create a function
def patch(f):
    "Decorator: add `f` to the first parameter's class (based on f's type annotations)"
    cls = next(iter(f.__annotations__.values()))
    nf = copy.copy(f)
    functools.update_wrapper(nf,f)
    nf.__qualname__ = f"{cls.__name__}.{f.__name__}"
    setattr(cls, f.__name__, nf)
    return f

#######################
# create a function whose first parameter is a class
def func(x:_T2, a:bool):
    "test"
    return a+2

#######################
# manually apply decorator to the function above
# so that func becomes a method of _T2
func = patch(func)

#######################
# test the decorated function
t = _T2(1) # create a _T2 instance, t 
test_eq(t.func(1), 3) # this t has a method func
test_eq(t.func.__qualname__, '_T2.func')

#######################
# apply decorator with syntatic sugar
@patch
def func(x:_T2, a:bool):
    "test"
    return a+2

t = _T2(1)
test_eq(t.func(1), 3)
test_eq(t.func.__qualname__, '_T2.func')
