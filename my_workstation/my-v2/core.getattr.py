from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

##################
# all dir, dt and additional together into a single list
def custom_dir(c, add:List):
    "Implement custom `__dir__`, adding `add` to `cls`"
    return dir(type(c)) + list(c.__dict__.keys()) + add

##################
# providing any subclass with two Methods
# 1. class attributes
#       a. _xtra=[] is a class attribute
#       b. defautl is a inexplicit class attribute (not specified)
# 2. __getattr__(self, k)
#       a. make sure _xtra is not empty;
#       b. in fact `default` attribute must exist too
#       c. if k is in _xtra, then return self.default.k
#       d. otherwise, raise AttributeError on k
# 3. __dir__(self) to bring dir(self), dt(self), and _xtra into a single list

class GetAttr:
    "Inherit from this to have all attr accesses in `self._xtra` passed down to `self.default`"
    _xtra=[]
    def __getattr__(self,k):
        assert self._xtra, "Inherited from `GetAttr` but no `_xtra` attrs listed"
        ###################
        # make_uncool
        if k in self._xtra:
            return getattr(self.default, k)
        raise AttributeError(k)

    # over write __dir__ to GetAttr.__dir__: print out all dr, dt and _xtra together
    def __dir__(self): return custom_dir(self, self._xtra)


class _C(GetAttr): default,_xtra = 'Hi',['lower']

t = _C()
t.default
t._xtra

############
# the following two are exactly the same
t.__getattr__('lower')
t.lower

# actually running the method
t.lower()
test_eq(t.lower(), 'hi')

# test on dir() or __dir__()
dir(t)
assert 'lower' in dir(t)

###################
# test error or Exception
test_fail(lambda: t.upper())
t.__getattr__('upper')
t.upper()

###################
# the actual practical usage of custom_dir and GetAttr
# 1. enable a subclass to take all its methods into its __dir__ using custom_dir
# 2. access additional methods from _xtra using __getattr__
