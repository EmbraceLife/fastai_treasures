from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
from local.data.pipeline import Item
# export
class Transform():
    "A function that `encodes` if `filt` matches, and optionally `decodes`, with an optional `setup`"

    order,assoc,filt,_is_setup,_done_setup,mask,is_tuple,prev = [0]+[None]*7


    def __init__(self, encodes=None, mask=None, is_tuple=None, **kwargs):
        """
        get `encodes` `decodes` ready
        get `order`, `mask`, `is_tuple` ready
        get other attributes ready
        """
        if encodes is not None:
            self.encodes=encodes
            if hasattr(encodes,'order'): self.order=encodes.order
        self.mask,self.is_tuple = mask,is_tuple
        for k,v in kwargs.items(): setattr(self, k, v)

    def setup(self, items=None):

        "Override `setups` for setup behavior"

        if self._is_setup: return
        self._is_setup = True
        self.setups(items)
        self._done_setup = True

    def _masked(self,b):
        """
        if `self.mask` is None but `self.is_tuple` is True,
        then make `mask` = [True, False ....];
        otherwise, `mask` = `self.mask`
        then `zip(b, mask)`
        """
        mask = [i==0 for i in range_of(b)] if self.mask is None and self.is_tuple else self.mask
        return zip(b,mask)

    def _apply(self, f, b, filt, **kwargs):
        """
        to apply `f` onto `b` given `filt` and `kwargs`
        1. if `filt` does not match, just return `b`
        2. if `self.is_tuple` is False or None, apply `f` on `b` with `kwargs`
        3. in other cases,....
        """
        if not self._filt_match(filt): return b
        if not self.is_tuple: return f(b, **kwargs)
        return tuple(f(o, **kwargs) if p else o for o,p in self._masked(b))

    def _filt_match(self, filt):
        "return true if `self.filt` is None, or `self.filt==filt`"
        return self.filt is None or self.filt==filt


    def __call__(self, b, filt=None, **kwargs):
        """
        to apply `self.encodes` onto `b` given `filt` and other `kwargs`
        """
        return self._apply(self.encodes, b, filt, **kwargs)

    def decode  (self, b, filt=None, **kwargs):

        "_apply `self.decodes` to `b`"

        return self._apply(self.decodes, b, filt, **kwargs)

    def show(self, o, filt=None, **kwargs):

        "Call `assoc.shows` with decoded `o`"

        od = self.decode(o, filt=filt)
        if self.assoc: return self.assoc.show(od, **kwargs)
        elif self.prev: return self.prev.show(od, filt=filt, **kwargs)

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

    def setups(self, items):

        "Override to implement custom setup behavior"

        pass

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


# wrap `Transform.__init__()` into a lambda func
negtfm = lambda: Transform(operator.neg, decodes=operator.neg, assoc=Item)
floattfm = lambda: Transform(float,decodes=int,assoc=Item)
# call `Transform.__init__()`: `encode`, `decode`, `assoc` are used to instantiate; print out with __repr__
tfm = negtfm(); tfm
start = 4
# `Transform.__call__(start)` => `_apply(encodes, start)`
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


####################
# official and compact
class Transform():
    order,assoc,filt,_is_setup,_done_setup,mask,is_tuple,prev = [0]+[None]*7
    def __init__(self, encodes=None, mask=None, is_tuple=None, **kwargs):
        if encodes is not None:
            self.encodes=encodes
            if hasattr(encodes,'order'): self.order=encodes.order
        self.mask,self.is_tuple = mask,is_tuple
        for k,v in kwargs.items(): setattr(self, k, v)

    def setup(self, items=None):
        if self._is_setup: return
        self._is_setup = True
        self.setups(items)
        self._done_setup = True

    def _masked(self,b):
        mask = [i==0 for i in range_of(b)] if self.mask is None and self.is_tuple else self.mask
        return zip(b,mask)

    def _apply(self, f, b, filt, **kwargs):
        if not self._filt_match(filt): return b
        if not self.is_tuple: return f(b, **kwargs)
        return tuple(f(o, **kwargs) if p else o for o,p in self._masked(b))

    def _filt_match(self, filt): return self.filt is None or self.filt==filt
    def __call__(self, b, filt=None, **kwargs): return self._apply(self.encodes, b, filt, **kwargs)
    def decode  (self, b, filt=None, **kwargs): return self._apply(self.decodes, b, filt, **kwargs)

    def show(self, o, filt=None, **kwargs):
        od = self.decode(o, filt=filt)
        if self.assoc: return self.assoc.show(od, **kwargs)
        elif self.prev: return self.prev.show(od, filt=filt, **kwargs)

    @classmethod
    def create(cls, f, filt=None): return f if isinstance(f,Transform) else cls(f)
    def __getitem__(self, x): return self(x) # So it can be used as a `Dataset`
    def decodes(self, o, *args, **kwargs): return o
    def setups(self, items): pass
    def __repr__(self): return str(self.encodes) if self.__class__==Transform else str(self.__class__)
    def set_tupled(self, tf=True): self.is_tuple = ifnone(self.is_tuple,tf)
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
