from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

################################
# create a decorator for class
def newchk(cls):
    "Class decorator to avoid recreating object passed to constructor"
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
t1 = _T(1)
t1 = _T(1)
#################################
# decorator with syntatic sugar
# with a little help
@newchk
class _T():
    "Testing"
    def __init__(self, o=None): self.foo = getattr(o,'foo',0) + 1

# We can make the world a better place
t1 = _T(1)
t1.foo
t2 = _T(t1)
t2.foo
t1 = _T(1)
t1 = _T(1)
################################
# made_uncool
# apply decorator to the class above
_T = newchk(_T)

t = _T(1)
# since t is an instance, so just return t rather than create anew
t2 = _T(t)

#################################
str(inspect.signature(_T))
