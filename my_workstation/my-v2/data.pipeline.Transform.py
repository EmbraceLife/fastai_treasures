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
        mask = [i==0 for i in range_of(b)] if self.mask is None and self.is_tuple else self.mask
        return zip(b,mask)

    def _apply(self, f, b, filt, **kwargs):
        """
        to apply `f` onto `b` given `filt` and `kwargs`
        1. if `filt` does not match, just return `b`
        2. if `self.is_tuple` is False or None, apply `f` on `b` with `kwargs`
        3. in other cases,
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
negtfm = lambda: Transform(operator.neg, decodes=operator.neg)
floattfm = lambda: Transform(float,decodes=int,assoc=Item)

# `Transform.__init__()`: `encode`, `decode`, `assoc` are used to instantiate
tfm = negtfm()

# apply Transform onto 4
start = 4
# `Transform.__call__` is called to execute `Transform.encodes()`
t = tfm(start)
test_eq(t, -4)

# `Transform.__getitem__(idx)` is to call `Transform.__call__(idx)`
tfm[start]
test_eq(t, tfm[start])

# `Transform.decode()`
tfm.decode(t)
test_eq(tfm.decode(t), start)

# `Transform.show()` is to decode back
floattfm().show(t)
test_stdout(lambda:floattfm().show(t), '-4')

# If a `Transform` has a `prev` attr, it will be recursively searched to
# find an `assoc`, e.g. for using with `show`.

# to `Transform.__init__`
tfm1 = floattfm()
tfm2 = negtfm()

# to `Transform.__call__` on `encodes` which `float` to apply on value 4
t1 = tfm1(start)

# add an instance of Transform to `tfm2.prev`
tfm2.prev = tfm1

# to `Transform.__call__` on `encodes` which `neg` to apply on outcome `t1`
t2 = tfm2(t1)

# `Transform.show` is to decode back, and with `tfm2.prev` defined
# decode func is to be `tfm1`

tfm2.show(t2)
test_stdout(lambda:tfm2.show(t2), str(start))


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
