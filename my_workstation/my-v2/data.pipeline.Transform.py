from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
from local.data.pipeline import Item

##############################################################################
class Transform():
    """
    "A function that `encodes` if `filt` matches, and optionally `decodes`, with an optional `setup`"

    1. every tfm's `order` default to 0
    2. `assoc`, `is_tuple`, `prev` default to None
    3. `filt`, `mask`, default to None
    4. `_is_setup`,`_done_setup`, default to None
    """
    order,assoc,filt,_is_setup,_done_setup,mask,is_tuple,prev = [0]+[None]*7

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


    def __init__(self, encodes=None, mask=None, is_tuple=None):
        """
        purpose:
        1. what are needed to create a Tfm object?
        2. prepare encodes = forward tfm
            2.1 self.encodes = encodes
            2.2 self.order = encodes.order
        3. prepare some properties for later use
            3.1 self.mask = mask = None
            3.2 self.is_tuple = is_tuple = None
        """
        self.mask,self.is_tuple = mask,is_tuple
        if encodes:
            self.encodes=encodes
            self.order = getattr(encodes,'order',0)
# Examples on the usage of `create()` for instantiate a new instance of Transform
Transform.create(operator.neg)
tfm = Transform(encodes=None, mask=None, is_tuple=None);tfm
test_fail(lambda: tfm.encodes, contains="no attribute 'encodes'")
tfm1 = tfm.create(operator.neg);tfm1
tfm1.encodes

# Examples: mk_class makes creating tfm super easy and convenient
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
member(negtfm) # both class is type
member(Transform) # both class is type
issubclass(negtfm, Transform)
# this is actually mk_class._init() executing,
# no additional attributes to be added

###################
# Examples on instance of negtfm (as subclass of Transform) can't use create properly
tfm = negtfm()
isinstance(tfm, negtfm)
isinstance(tfm, Transform)# show_doc(negtfm)
hasattr(tfm, 'create')
test_fail(lambda: tfm.create(float)) # intend `cls` => Transform, but mk_class
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


@patch
def setups(cls:Transform, items):
    """
    purpose:
    1. whatever we want to make further custom preparation on attributes
    """
    return noop(items)

# Examples
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
member(negtfm) # both class is type
member(Transform) # both class is type
issubclass(negtfm, Transform)
# this is actually mk_class._init() executing,
# no additional attributes to be added
tfm = negtfm()
# show_doc(negtfm)
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
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
issubclass(negtfm, Transform)
getattr(negtfm, '_masked', 0)
# this is actually mk_class._init() executing,
# no additional attributes to be added
tfm = negtfm()
tfm.is_tuple
tfm = negtfm(is_tuple=True)# mk_class.__init__ makes add attributes super easy
tfm.mask # to make sure it is None
tfm.is_tuple
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
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
issubclass(negtfm, Transform)
getattr(negtfm, '_masked', 0)
# this is actually mk_class._init() executing,
# no additional attributes to be added
tfm = negtfm()
tfm.mask # to make sure it is None
tfm.is_tuple = True # make sure this is True
b = [1,2,3]
set(tfm._masked([1,2,3]))
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
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
issubclass(negtfm, Transform)
getattr(negtfm, '_masked', 0)
# this is actually mk_class._init() executing to create an instance
# no additional attributes to be added
tfm = negtfm()
tfm.mask # to make sure it is None
tfm.is_tuple = True # make sure this is True
b = [1,2,3]
set(tfm._masked([1,2,3]))
tfm.filt
tfm.is_tuple = True
tfm(L(1,2,3))
tfm.is_tuple = None
tfm(3)

##############################################################################
@patch
def decode(cls:Transform, b, filt=None, **kwargs):
    """
    purpose:
    1. after encoding, sometimes, we want the original state back
    2. so we need to do decoding
    3. the logic is the same to encoding or __call__
        3.3 `_apply`, `decodes`, to `b`
    """
    return cls._apply(cls.decodes, b, filt, **kwargs)

# Examples
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
issubclass(negtfm, Transform)
getattr(negtfm, '_masked', 0)
# this is actually mk_class._init() executing,
# no additional attributes to be added
tfm = negtfm()
tfm.mask # to make sure it is None
tfm.is_tuple = True # make sure this is True
b = [1,2,3]
set(tfm._masked([1,2,3]))
tfm.filt
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
    # this show is more flexible than the one below
    elif cls.prev: return cls.prev.show(od, filt=filt, **kwargs)

# Examples 1
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
tfm = floattfm()
t = tfm(4); t # this is executing __call__(4)
tfm.show(t) # run decode first, and Item.show()
# Examples 2
tfm = negtfm()
t = tfm(4);t
tfm.show(t) # no tfm.prev nor tfm.assoc available to display
borrow = floattfm() # get floattfm which as assoc
tfm.assoc = borrow.assoc # borrow it
tfm.show(t) # now it can display with Item.show
# Examples 3
tfm1 = floattfm()
tfm2 = negtfm()
t = tfm2(tfm1(3)); t
tfm2.decode(t)
tfm2.show(t) # negtfm has no assoc, can't display
tfm2.prev = tfm1
# it decodes to 3.0, then move onto prev/floattfm to decode and display
tfm2.show(t)


##############################################################################
@patch
def __getitem__(cls:Transform, x):
    """
    purpose:
    1. well, getitem is essentially __call__ at idx
    """

    return cls(x) # So it can be used as a `Dataset`

# Examples 1
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
tfm = floattfm()
tfm(4)
tfm[5]
tfm.is_tuple = True
tfm([1,2,3])
tfm[4,4,5]
member(tfm)

##############################################################################
@patch
def decodes(cls:Transform, o, *args, **kwargs):

    "Override to implement custom decoding"
    return o

# simple usage of decodes and overwrite
tfm = Transform(encodes=None, mask=None, is_tuple=None)
tfm.decodes(5) # Transform.decodes original state
tfm.decodes = operator.neg
tfm.decodes(5)

# example to overwrite Transform.decodes with mk_class
mk_class('negtfm', sup=Transform, encodes=operator.neg, decodes=operator.neg)
tfm = negtfm() # created an instance of negtfm, a subclass of Transform
tfm.decodes # overwrite Transform.decodes
tfm.decodes(5)

##############################################################################
@patch
def __repr__(cls:Transform):
    """
    purpose:
    1. whenever print out an object, we want to see either
        1.1 all the encodes methods if it is instance of Transform or subclass
        1.2 just the class of the object
    """

    return str(cls.encodes) if cls.__class__==Transform or issubclass(cls.__class__, Transform) else str(cls.__class__)

# Examples
mk_class('negtfm', sup=Transform, encodes=operator.neg, decodes=operator.neg)
tfm = negtfm()
negtfm.encodes
tfm.__repr__()
tfm

##############################################################################
@patch
def find_assoc(cls:Transform):
    """
    purpose:
    1. because we rely on `assoc`, e.g., `Item` to `show`
    2. but not always the case the current tfm has `assoc`
    3. in this case we need to search `assoc` in the `prev` tfm
    so, `find_assoc` search and return `assoc` or None from current or prev
    """
    return cls.assoc if cls.assoc else cls.prev.find_assoc() if cls.prev else None

# Examples
mk_class('negtfm', sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
tfm1 = negtfm()
tfm2 = floattfm()
tfm1.find_assoc()
tfm2.find_assoc()
tfm1.prev = tfm2
tfm1.find_assoc()

##############################################################################
@patch
def set_tupled(cls:Transform, tf=True):
    """
    purpose:
    1. `cls.is_tuple` is to control scalar or multiple computation
    2. the default value is None,
    3. if `cls.is_tuple` is None, it can be turned to True or False by `tf`
    4. but once `cls.is_tuple` is no longer None, it won't be changed by
        - this func `set_tupled` anymore
    5. you have to directly do `cls.is_tuple = False/True` to change it
    """
    cls.is_tuple = ifnone(cls.is_tuple,tf)

# Examples
mk_class('negtfm', sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
tfm1 = negtfm()
tfm2 = floattfm()
tfm1.is_tuple
tfm1.set_tupled()
tfm1.is_tuple
tfm1.set_tupled(tf=False)
tfm1.is_tuple = False

##############################################################################
class _AddTfm(Transform): # create a subclass to Transform
    assoc=Item # assoc is class attribute, available to all objects
    def encodes(self, x, a=1): return x+a
    def decodes(self, x, a=1): return x-a

addt  = _AddTfm(); addt.__dict__
addt.assoc
addt.encodes(3)
addt(3)
addt.decodes(4, a=1)
addt.show(4)
addt.filt=1
addt(3,filt=1) # still not sure about the usage of `filt`
addt(3,filt=0) # but maybe this is how we should use `filt`: 1 or 0

###How to make sure of `mask`
show_doc(Transform.__init__)
addt  = _AddTfm(is_tuple=True)
start = (1,2,3)
t = addt(start);t # only apply to the first item
addt.decode(t)
tfm = _AddTfm(is_tuple=True, mask=(True,True,True)) # apply to all three items
start = (1,2,3)
t = tfm(start);t
tfm.decode(t)
