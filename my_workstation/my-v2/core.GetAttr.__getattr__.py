from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


class GetAttr:
    """
    why need `GetAttr`
    - want class `a` to use class `b` methods
    - but don't want to copy those methods into 'a'

    how to use `GetAttr`?
    - make class `a` a subclass of `GetAttr`
    - having `b` instance assigned to `a.default`
    - having `b` methods stored in `a._xtra` as strings
    - then you can call `a_instance.b_method()`
    - `a_instance.__dir__` list all methods including b's

    """
    _xtra=[]
    def __getattr__(self,k):
        """
        why `__getattr__`?
        - class a instance can get a method 'k' from class b

        how does `__getattr__` work?
        0. when calling `a_instance.b_method()`, it runs below
        1. make sure `_xtra` is not None
        2. allow `a.k` to return `a.default.k`
        3. if `k` is not in _xtra, raise AttributeError
        """
        assert self._xtra, "Inherited from `GetAttr` but no `_xtra` attrs listed"
        if k in self._xtra: return getattr(self.default, k)
        raise AttributeError(k)

    def __dir__(self): return custom_dir(self, self._xtra)

show_doc(GetAttr)
############################################
# how _C borrow str.lower to use
class _C(GetAttr): default,_xtra = 'Hi',['lower']

t = _C()
t.default
t._xtra
t.__getattr__('lower')
t.__getattr__('lower')()
t.lower()
test_fail(lambda: t.upper(), contains='upper')

##########################################
# how L borrow list.sort to use
x = [1,1,0,5,0,3]
x = list(OrderedDict.fromkeys(x).keys()); x
x = L(8,9) + x
x.sort(); x
