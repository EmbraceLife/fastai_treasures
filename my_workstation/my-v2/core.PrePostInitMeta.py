from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

# check the official source
show_doc(PrePostInitMeta, title_level=3)

class PrePostInitMeta(type):
    """
    "A metaclass that calls optional `__pre_init__` and `__post_init__` methods"

    Why need `PrePostInitMeta`?
    - not only run `__init__`, but also
    - automatically run `__pre_init__`, `__post_init__`

    How to use `PrePostInitMeta`?
    - create a subclass to `PrePostInitMeta`
    - you can add `__pre_init__` and `__post_init__` to `__init__`
    - program will run them in the order of `__pre_init__`, `__init__` and `__post_init__`
    - if any of them is missing, a `_pass()` method will run instead

    How to create `PrePostInitMeta`?
    - how to lay out the logic flow?
    - use pdb break at the first line of `__new__`
    - basically `__new__` run before running `t=_T()`
    - to prepare all the additional methods of `x` or `_T`
    """
    def __new__(cls, name, bases, dct):
        # pdb break here to run the hidden codes
        x = super().__new__(cls, name, bases, dct)
        def _pass(self, *args,**kwargs): pass
        for o in ('__init__', '__pre_init__', '__post_init__'):
            if not hasattr(x,o): setattr(x,o,_pass)
        old_init = x.__init__

        @functools.wraps(old_init)
        def _init(self,*args,**kwargs):
            self.__pre_init__()
            old_init(self, *args,**kwargs)
            self.__post_init__()
        setattr(x, '__init__', _init)
        return x


# simple but standard example
class _T(metaclass=PrePostInitMeta):
    def __pre_init__(self):  self.a  = 0; assert self.a==0
    def __init__(self):      self.a += 1; assert self.a==1
    def __post_init__(self): self.a += 1; assert self.a==2

t = _T() #pdb
t.a

# what would happen when lacking __pre_init__
class _T(metaclass=PrePostInitMeta):
    def __pre_init__(self):  self.a  = 0; assert self.a==0
    def __init__(self):      self.a += 1; assert self.a==1
    # def __post_init__(self): self.a += 1; assert self.a==2

t = _T()#pdb
t.a
