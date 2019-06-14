from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
from local.data.pipeline import Item

##############################################################################
class Transform():
    "A function that `encodes` if `filt` matches, and optionally `decodes`, with an optional `setup`"

    # every tfm.order default to 0
    # assoc, is_tuple, prev default to None
    # filt, mask, default to None
    #_is_setup,_done_setup, default to None
    order,assoc,filt,_is_setup,_done_setup,mask,is_tuple,prev = [0]+[None]*7


    def __init__(self, encodes=None, mask=None, is_tuple=None, **kwargs):
        """
        purpose:
        1. what are needed to create a Tfm object?
        2. prepare encodes = forward tfm
            2.1 self.encodes = encodes
            2.2 self.order = encodes.order
        3. prepare some properties for later use
            3.1 self.mask = mask = None
            3.2 self.is_tuple = is_tuple = None
        4. prepare other properties from **kwargs
            4.1 self.k = v (`k, v in kwargs.items()`)
        """
        if encodes is not None:
            self.encodes=encodes
            if hasattr(encodes,'order'): self.order=encodes.order
        self.mask,self.is_tuple = mask,is_tuple
        for k,v in kwargs.items(): setattr(self, k, v)

# Examples
# how to instantiate a Tfm object
negtfm = lambda: Transform(operator.neg, # named arg 'encodes'
                            decodes=operator.neg, # from **kwargs, backward tfm
                            assoc=Item) # from **kwargs, hidden
floattfm = lambda: Transform(float, # named arg 'encodes'
                            decodes=int,# from **kwargs, hidden
                            assoc=Item)# from **kwargs, hidden
tfm = negtfm(); tfm # default __repr__, not yet overwritten, not informative
tfm = negtfm(); tfm
member(tfm) # to check on

##############################################################################
@patch
def setup(cls:Transform, items=None):
    """
    purpose:
    1. __init__ prepares `encodes`, `is_tuple`, `mask` and other attributes
    2. but we may need some custom setups to be done
        2.1 after running `cls.setup(items)`, we mark `cls._is_setup`, `cls._done_setup` True
        2.2 we also run custom `cls.setups(items)` function
        2.3 `items` are things to be setup about
    3. no matter whatever `cls.setups(items)` returns, nothing return here
    """
    if cls._is_setup: return
    cls._is_setup = True
    cls.setups(items)
    cls._done_setup = True

##############################################################################
@patch
def setups(cls:Transform, items):
    """
    purpose:
    1. whatever we want to make further custom preparation on attributes
    """
    return noop(items)

# Examples
negtfm = lambda: Transform(operator.neg, # named arg 'encodes'
                            decodes=operator.neg, # from **kwargs, backward tfm
                            assoc=Item) # from **kwargs, hidden
tfm = negtfm(); tfm
member(tfm) # to check on
tfm.setup(1)
tfm.setups(1)
tfm._is_setup
noop(1)

##############################################################################
@patch
def _masked(cls:Transform,b):
    """
    Purpose:
    1. _masked is to create mask data from `b`
    2. if what we face is
        2.1 don't have `cls.mask` available,
        2.2 have to deal with more data samples, as `cls.is_tuple` is true
    3. then create a list of [True, False, ...], and assign to `mask`
        3.1 only the first item is `True`, the rest is `False`
        3.2 the length of this list is `len(b)`
    4. if 2.1 or 2.2 not met, just assign `self.mask` to `mask`
    5. return zip(b, mask)
        5.1 it is like provide a list of T/F as mask for `b`
        5.2 but why only the first item is True?
    """
    mask = [i==0 for i in range_of(b)] if cls.mask is None and cls.is_tuple else cls.mask
    return zip(b,mask)

# Examples
negtfm = lambda: Transform(operator.neg, # named arg 'encodes'
                            decodes=operator.neg, # from **kwargs, backward tfm
                            assoc=Item) # from **kwargs, hidden
tfm = negtfm(); tfm
tfm.mask # to make sure it is None
tfm.is_tuple = True # make sure this is True
b = [1,2,3]
set(tfm._masked([1,2,3]))

##############################################################################
@patch
def _apply(cls:Transform, f, b, filt, **kwargs):
    """
    purpose:
    1. basically to apply `f` on `b`
    2. but `b` can be scalar or multiple/tuple
    3. if `b` is scalar not tuple, just return `f(b, **kwargs)`
    4. if `b` is tuple,
        4.1 we mask `b` so that only `b[0]` get applied with `f`
        4.2 store `f(b[0])` and `b[1:]` into a tuple, and return it
    5. if `filt` doesn't match, just return `b`
    """
    if not cls._filt_match(filt): return b
    if not cls.is_tuple: return f(b, **kwargs)
    return tuple(f(o, **kwargs) if p else o for o,p in cls._masked(b))

@patch
def _filt_match(cls:Transform, filt):
    """
    purpose:
    1. filt matches(or True) means two possibilities
        1.1 either `cls.filt` is `None`
        1.2 or `cls.filt == filt`
    """
    return cls.filt is None or cls.filt==filt

# Examples
negtfm = lambda: Transform(operator.neg, # named arg 'encodes'
                            decodes=operator.neg, # from **kwargs, backward tfm
                            assoc=Item) # from **kwargs, hidden
tfm = negtfm(); tfm
tfm.filt
tfm.is_tuple = True
tfm._apply(float, [1,2,3], None)
tfm._apply(str, [1,2,3], None)

##############################################################################
@patch
def __call__(cls:Transform, b, filt=None, **kwargs):
    """
    purpose:
    1. `tfm()` or `tfm.__call__` is reserved for most used actions
    2. it means to do tranformation or forward transformation or encodes
    3. so we shall `_apply` `encodes` to `b`:
        3.1. `cls.encodes` is `f` for actual tranformation
        3.2. `b` is about data
        3.3. `filt` and `is_tuple` controls to return `b` or ...
    """
    return cls._apply(cls.encodes, b, filt, **kwargs)

# Examples
negtfm = lambda: Transform(operator.neg, # named arg 'encodes'
                            decodes=operator.neg, # from **kwargs, backward tfm
                            assoc=Item) # from **kwargs, hidden
tfm = negtfm(); tfm
tfm.filt
tfm.is_tuple = True
tfm(L(1,2,3))
tfm.is_tuple = None
tfm(3)

##############################################################################
@patch
def decode  (cls:Transform, b, filt=None, **kwargs):
    """
    purpose:
    1. after encoding, sometimes, we want the original state back
    2. so we need to do decoding
    3. the logic is the same to encoding or __call__
        3.3 `_apply`, `decodes`, to `b`
    """
    return cls._apply(cls.decodes, b, filt, **kwargs)

# Examples
negtfm = lambda: Transform(operator.neg, # named arg 'encodes'
                            decodes=operator.neg, # from **kwargs, backward tfm
                            assoc=Item) # from **kwargs, hidden
tfm = negtfm(); tfm
tfm.filt
tfm.is_tuple = True
t = tfm(L(1,2,3)); t
tfm.decode(t)
tfm.is_tuple = None
t = tfm(3); t
tfm.decode(t)


##############################################################################
@patch
def show(cls:Transform, o, filt=None, **kwargs):

    "Call `assoc.shows` with decoded `o`"

    od = cls.decode(o, filt=filt)
    if cls.assoc: return cls.assoc.show(od, **kwargs)
    elif cls.prev: return cls.prev.show(od, filt=filt, **kwargs)

@classmethod
def create(cls, f, filt=None):
    """
    if `f` is already an instance of `Transform`, just return `f`;
    if not, turn `f` into a `Transform`
    """
    if isinstance(f,Transform):
        return f
    else:
        return cls(f)

def __getitem__(self, x):
    """
    `Transform.__getitem__(idx)` is to call `Transform.__call__(idx)`
    """

    return self(x) # So it can be used as a `Dataset`

def decodes(self, o, *args, **kwargs):

    "Override to implement custom decoding"
    return o



def __repr__(self):
    """
    when printing out the `self` object,
    if self is an object of `Transform`, it returns its `encodes` method;
    if not, just return its class
    """
    if self.__class__==Transform:
        return str(self.encodes)
    else:
        str(self.__class__)

def set_tupled(self, tf=True):

    "Set `is_tuple` to `tf` if it was `None` (used internally by `TfmOver`)"

    self.is_tuple = ifnone(self.is_tuple,tf)
# %%
add_docs(Transform,
         "A function that `encodes` if `filt` matches, and optionally `decodes`, with an optional `setup`",
         create="classmethod: Turn `f` into a `Transform` unless it already is one",
         __call__="Call `self.encodes` unless `filt` is passed and it doesn't match `self.filt`",
         decode="Call `self.decodes` unless `filt` is passed and it doesn't match `self.filt`",
         decodes="Override to implement custom decoding",
         show="Call `assoc.shows` with decoded `o`",
         set_tupled="Set `is_tuple` to `tf` if it was `None` (used internally by `TfmOver`)",
         setup="Override `setups` for setup behavior",
         setups="Override to implement custom setup behavior")
# %% markdown
# In a transformation pipeline some steps need to be reversible - for instance,
# if you turn a string (such as *dog*) into an int (such as *1*) for modeling,
# then for display purposes you'll want to turn it back to a string again (e.g.
# when you have a prediction). In addition, you may wish to only run the
# transformation for a particular data subset, such as the training set.

# `Transform` provides all this functionality. `filt` is some dataset index
# (e.g. provided by `DataSource`), and you provide `encodes` and
# optional `decodes` functions for your code. You can pass `encodes` and
# `decodes` functions directly to the constructor
# for quickly creating simple transforms.

from local.data.pipeline import Transform
# wrap `Transform.__init__()` into a lambda func
negtfm = lambda: Transform(operator.neg, decodes=operator.neg, assoc=Item)
floattfm = lambda: Transform(float,decodes=int,assoc=Item)
# call `Transform.__init__()`: `encode`, `decode`, `assoc` are used to instantiate; print out with __repr__
tfm = negtfm(); tfm
start = [4,5,6]
# `Transform.__call__(start)` => `_apply(encodes, start)`
tfm.is_tuple = True
t = tfm(start); t
# `Transform.__getitem__(idx)` => `__call__(idx)` => `_apply(encodes,idx)`
tfm[start]
# `Transform.decode(t)` => '_apply(decodes, t)'
tfm.decode(t)
# `Transform.show(t)` => `od = decode(t)` + `Item.show(od)`
tfm.show(t)

# If a `Transform` has a `prev` attr, it will be recursively searched to
# find an `assoc`, e.g. for using with `show`.
tfm1 = floattfm()
tfm2 = negtfm()
# `Transform.__call__` => `_apply(float, 4)`
t1 = tfm1(start); t1
# add neg operator to be `tfm2.prev`
tfm2.prev = tfm1
tfm2.assoc = None
# `__call__(4.0)` => `_apply(neg, 4.0)`
t2 = tfm2(t1); t2
# tfm2 only has tfm2.prev, and tfm1 only has tfm1.assoc
# negtfm.show(t2) => od1 = _apply(neg, t2) + floatfm.show(od1)=> ...
# od2 = _apply(int, od1) + Item.show(od2)
tfm2.show(t2)

class _AddTfm(Transform): # Generally you'll subclass `Transform`
    assoc=Item # and `assoc`
    def encodes(self, x, a=1): return x+a # overwrite `encodes`
    def decodes(self, x, a=1): return x-a # overwrite `decodes`

addt  = _AddTfm()
start = 4
t = addt(start);t
addt.decode(5)
addt.show(t, filt=None)
addt.filt=1 # specify `filt`
addt(start,filt=1) # if `filt` matches or None, carry on `encode`
addt(start,filt=0) # if `filt` no match, then return `start`

addt  = _AddTfm(is_tuple=True)
start = (1,2,3)
addt.mask
list(addt._masked(start))
# _apply(encodes, start) => tuple(f(o, **kwargs) if p else o for o,p in self._masked(b))
t = addt(start); t
addt.decode(t)

tfm = _AddTfm(is_tuple=True, mask=(True,True,True))
start = (1,2,3)
tfm.mask
list(tfm._masked(start))
t = tfm(start);t
tfm.decode(t)
tfm.show(t, filt=None)
