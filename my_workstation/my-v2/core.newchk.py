from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

################################
# create a decorator for class
def newchk(cls):
    """
    "Class decorator to avoid recreating object passed to constructor"

    purpose:
    1. we want class constructor __init__ to be smarter:
        a. t = cls.__init__(value)
        b. t = cls.__init__(t)
    2. in other words, besides creating new instance,
        it should recognise existing instance and do nothing to it
    3. we want such smart feature to have easily obtained by any class

    steps
    1. _inner_new:
        a. if `x` is instance of `cls`, then mark it '1' and pass it to step 2
        b. if not instance, mark it '0' and pass a new object to step 2
    2. _inner_init:
        a. if mark == 1, return nothing
        b. if mark == 0, return a new instance of `cls` with args, kwargs
    """
    old_new,old_init  = cls.__new__,cls.__init__

    # to create a new object or return the existing one
    def _inner_new(cls, x=None, *args, **kwargs):
        if x is not None and isinstance(x,cls):
            x._newchk = 1
            return x
        res = old_new(cls)
        res._newchk = 0 # mark new as 0
        return res

    # initialize using old_init or return nothing
    def _inner_init(self, *args, **kwargs):
        if self._newchk: return
        old_init(self, *args, **kwargs)

    # wrap _inner_new around cls.__init__, assign to cls.__new__
    cls.__new__  = functools.update_wrapper(_inner_new,  cls.__init__)
    # wrap _inner_init around cls.__init__, assign to cls.__init__
    cls.__init__ = functools.update_wrapper(_inner_init, cls.__init__)
    return cls

################################
# Usually the world works like this
class _T():
    "Testing"
    def __init__(self, o=None): self.foo = getattr(o,'foo',0) + 1

t1 = _T(1)
t1.foo
t2 = _T(t1)
t2.foo
test_fail(lambda: test_is(t1, t2))

@newchk
class _T():
    "Testing"
    def __init__(self, o=None): self.foo = getattr(o,'foo',0) + 1

t1 = _T(1)
t1.foo
t2 = _T(t1)
t2.foo
test_is(t1, t2)

_T = newchk(_T)
