from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

import copy

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

########################
# a simple class with only __init__ method
class _T2():
    def __init__(self, o): self.foo = getattr(o,'foo',0) + 1

#######################
# Wishing a new world where we just define the new function,
# and it will add onto the class automatically
def func(x:_T2, a:bool):
    "test"
    return a+2

t = _T2(1)
t.__init__
test_fail(lambda: t.func, contains= "no attribute 'func'")

########################
# In this old world, we have to do the following
class _T2():
    def __init__(self, o): self.foo = getattr(o,'foo',0) + 1

    # add another function here
    def func(x:_T2, a:bool):
        "test"
        return a+2

t = _T2(1)
t.__init__
t.func


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
