from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L

def custom_dir(c, add:List):
    """
    purpose:
    1. sometimes want to see both `dir(c)` and `dict(c)`
    2. why don't we put them together and get them in one go?
    3. what if we even add/borrow some methods to use too?
        a. we put the additional/extrac methods into a list `add`
        b. in one go, we output the `dir, dict, add` together
    """
    return dir(type(c)) + list(c.__dict__.keys()) + add

custom_dir(int, list())[-2:]
class GetAttr:
    """
    purpose:
    1. ever want to borrow attributes or methods of class
        'b' for class 'a' to use
    2. without rewrite those methods/attributes inside 'a'
    3. subclass `GetAttr`, `a` can borrow `b`'s methods very easy
        a. having `b` instance assigned to `a.default`
        b. having `b` methods/attributes stored in `a._xtra`
            as strings
        c. then you can call `b.methods` as if it is `a.methods`
        d. note: such borrowed methods are bound to `a.default`
            !!!! need to see more actions !!!
    4. also we want to see all methods/attributes of 'a':
        dir, dict, and _xtra
    """
    _xtra=[]
    def __getattr__(self,k):
        """
        steps:
        1. make sure `_xtra` is not None
        2. allow `a.k` to return `a.default.k`
        3. if `k` is not in _xtra, raise AttributeError
        """
        assert self._xtra, "Inherited from `GetAttr` but no `_xtra` attrs listed"
        if k in self._xtra:
            return getattr(self.default, k)
        raise AttributeError(k)

    def __dir__(self): return custom_dir(self, self._xtra)

############################################
# how _C borrow str.lower to use
class _C(GetAttr): default,_xtra = 'Hi',['lower']

t = _C()
t.default
t._xtra
t.__getattr__('lower')
t.lower
t.lower()
test_fail(lambda: t.upper(), contains='upper')

##########################################
# how L borrow list.sort to use
x = [1,1,0,5,0,3]
x = list(OrderedDict.fromkeys(x).keys()); x
x = L(8,9) + x
x.sort(); x
