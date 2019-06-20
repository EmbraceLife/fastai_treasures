from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

class NewChkMeta(PrePostInitMeta):
    """
    "Metaclass to avoid recreating object passed to constructor (plus all `PrePostInitMeta` functionality)"

    Why need NewChkMeta?
    - to ensure it won't create an instance twice

    How to use NewChkMeta?
    - use it as super class for any class you want with this feature

    How to debug?
    - # pdb break on the first line to see the logic flow
    - check values for cls, name, bases, dct, to see where we started x

    Note:
    - from `old_init(self, *args, **kwargs)` we enter `PrePostInitMeta` wrapper for `old_init`
    """
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        old_init,old_new = x.__init__,x.__new__

        @functools.wraps(old_init)
        def _new(cls, x=None, *args, **kwargs):
            if x is not None and isinstance(x,cls):
                x._newchk = 1
                return x
            res = old_new(cls)
            res._newchk = 0
            return res

        @functools.wraps(old_init)
        def _init(self,*args,**kwargs):
            if self._newchk: return
            old_init(self, *args, **kwargs)

        x.__init__,x.__new__ = _init,_new
        return x

class _T(metaclass=NewChkMeta):
    "Testing"
    def __init__(self, o=None): self.foo = getattr(o,'foo',0) + 1

class _T2():
    def __init__(self, o): self.foo = getattr(o,'foo',0) + 1

# example shows that passing an instance won't create a new instance
# but only return the old instance
t = _T(1)
test_eq(t.foo,1)
t2 = _T(t)
test_eq(t2.foo,1)
test_is(t,t2) # they are the same instance


t = _T2(1)
test_eq(t.foo,1)
t2 = _T2(t)
test_eq(t2.foo,2)
# test_is(t,t2) # they aren't the same thing


test_eq(_T.__doc__, "Testing")
test_eq(str(inspect.signature(_T)), '(o=None)')
