from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import Transform, Item
############################################################################
def _set_tupled(tfms, m=True):
    """
    purpose:
    1. `Transform.set_tupled` turns the single current `tfm.is_tuple` True or False.
    2. What if we want to turn all the tfms at hand `is_tuple` True?
    3. this stand alone func `_set_tupled(tfms, m=True)` can do just that!
        3.1 put all `tfms` under `L` management
        3.2 loop through each `tfm`,
            a. if they are `Transform` instance, they can run `set_tupled(True)`
            b. if they aren't, run `noop(True)`
    4. return all the `tfms`
    """
    tfms = L(tfms)
    for t in tfms: getattr(t,'set_tupled',noop)(m)
    return tfms

tfms = L([operator.neg, float]).mapped(Transform.create)
_set_tupled(tfms)
tfms[0].is_tuple
tfms[1].is_tuple
############################################################################

@newchk
class Pipeline(Transform):
    """
    purpose:
    - why need `Pipeline`?
    1. `Transform` is create and deal with single tfm
    2. `Pipeline` is to create and deal with a bunch
    """

    def __init__(self, tfms=None):
        """
        purpose:
        - construct what exactly?
        1. not a single Tranform instance but a bunch of

        steps:
        0. @newchk ensure `Pipeline(p)` return `p` if `p` is a pipeline
        0. what are needed to become a Pipeline instance?
        0. we need a lot of funcs acting as `tfms`
            0.1 use `L` to organize `tfms`
            0.2 turn every `tfms` into a `Transform` instance
        0. assign this list of `Transform` instance under `self._tfms`
        0. leave `self.tfms` as `[]` empty
        """
        self.tfms,self._tfms = [],L(tfms).mapped(Transform.create)

    @property
    def assoc(self): return self.tfms[-1].find_assoc()

p = Pipeline(tfms=[operator.neg, float])
p.tfms
p._tfms

############################################################################
@patch
def setups(cls:Pipeline, items=None):
    """
    purpose:
    - why need `setups`?
    1. `__init__` does basic construction
    2. `__init__` may not be enough for further processing
    3. more importantly, `Pipeline` inherit `setups` from `Transform.setups`, and overwrite!!
    4. through overwriting `setups`, `Pipeline.add` is created

    steps:
    1. after a pipeline is constructed, we still need basic setups
        1.1 transfer `cls._tfms` to `tfms`, not `self.tfms`
        1.2 assign None to `cls._tfms`
    2. more important setups is `cls.add` `tfms` onto `self.tfms`
        2.1 at the same time, ask each `tfm` to set itself up
        2.2 it means for each `tfm` to do sth about `items`
        for details, see `Pipeline.add`
    """
    tfms,cls._tfms = cls._tfms,None
    cls.add(tfms, items)

@patch
def add(cls:Pipeline, tfms, items=None):
    """
    purpose:
    1. `add` is to add `tfms` onto `cls.tfms`
    2. but there are some hidden and important tasks as well
        2.1 all `tfms` are sorted by `order`, and loop them
        2.2 set earlier `tfm` to be later tfm's `prev`
        2.3 add each `tfm` onto `self.tfms`
        2.3 if a `tfm` has `setup` method, run it on `items`
    3. there is no return in this func
    """
    prev=None
    for t in sorted(L(tfms), key=lambda o: getattr(o, 'order', 0)):
        if prev: t.prev=prev
        prev=t
        cls.tfms.append(t)
        if hasattr(t, 'setup'): t.setup(items) # Transform.setup

p = Pipeline(tfms=[operator.neg, float])
p.setups() # we didn't get any `items` as no `tfm.setups` actually do anything
p.tfms
p.tfms[0].prev
p.tfms[1].prev

############################################################################
@patch
def composed(cls:Pipeline, x, rev=False, fname='__call__', **kwargs):
    """
    oneliner:
    - `composed` is to apply all `tfms` on `x` and return `x`

    purpose:
    0. we have `Transform._apply` to apply a tfm on a scalar or multiples
    0. how do we apply many tfms to a scalar or multiple?
        1. loop through all tfms is a must
        2. before looping, we better have all tfms sorted out with `cls.setups()`
            a. to keep `cls._tfms` empty
            b. to have `cls.tfms` sorted by `order`
            c. it is nicer with option to reverse tfms order
        3. loop each `tfm`,
            a. apply `tfm.fname` on `x` and assign back to `x`
    """
    assert not cls._tfms, "Run `setup` before calling `Pipeline`"
    tfms = reversed(cls.tfms) if rev else cls.tfms
    for f in tfms: x = opt_call(f, fname, x, **kwargs)
    return x

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3)
flt = floattfm(is_tuple=True, mask=[True]*3)
p = Pipeline([neg, flt])
p.setups() # we didn't get any `items` as no `tfm.setups` actually do anything
p.composed([1,2,3])
p.composed([1,2,3], rev=True)

############################################################################
@patch
def __call__(cls:Pipeline, x, **kwargs):
    "`__call__(x)` is to execute `composed(x)`"
    return cls.composed(x, **kwargs)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3)
flt = floattfm(is_tuple=True, mask=[True]*3)
p = Pipeline([neg, flt])
p.setups() # we didn't get any `items` as no `tfm.setups` actually do anything
p.composed([1,2,3])
p([1,2,3])

############################################################################
@patch
def __getitem__(cls:Pipeline, x):
    "to `self[x]` is to `self(x)`"
    return cls(x)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3)
flt = floattfm(is_tuple=True, mask=[True]*3)
p = Pipeline([neg, flt])
p.setups() # we didn't get any `items` as no `tfm.setups` actually do anything
p[10,13,16]


############################################################################
@patch
def decode(cls:Pipeline, x, **kwargs):
    """
    "self.decode(x) => self.composed(x, rev=T, fname='decode')"

    purpose:
    1. since `cls.composed(fname='__call__')` is to encode by many tfms
    2. naturally decode them all, we use `cls.composed` with `fname='decode'`
    """
    return cls.composed(x, rev=True, fname='decode', **kwargs)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3)
flt = floattfm(is_tuple=True, mask=[True]*3)
p = Pipeline([neg, flt])
p.setups() # we didn't get any `items` as no `tfm.setups` actually do anything
t = p.composed([1,2,3]);t
p.decode(t)
p.tfms[1].prev
p.tfms[0].prev

############################################################################
@patch
def decode_at(cls:Pipeline, idx):
    "decode + [idx], buy why do we need such a method, seemingly running in circle"
    return cls.decode(cls[idx])

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3)
flt = floattfm(is_tuple=True, mask=[True]*3)
p = Pipeline([neg, flt])
p.setups() # we didn't get any `items` as no `tfm.setups` actually do anything
p.decode_at([1,2,3])
p.decode(p[1,2,3])


############################################################################
@patch
def show_at(cls:Pipeline, idx):
    "show + [idx]"
    return cls.show(cls[idx])

@patch
def show(cls:Pipeline, o, *args, **kwargs):
    "decode all the way/all the tfms back, and show the result"
    return cls.tfms[-1].show(o, *args, **kwargs)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3, assoc=Item)
flt = floattfm(is_tuple=True, mask=[True]*3, assoc=None) # note: who has `assoc`
p = Pipeline([neg, flt])
p.setups() # we didn't get any `items` as no `tfm.setups` actually do anything
p.show_at([1,2,3])
p.show(p[1,2,3])

############################################################################
@patch
def __repr__(cls:Pipeline):
    "to print out all tfms"
    return str(cls.tfms)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3, assoc=Item)
flt = floattfm(is_tuple=True, mask=[True]*3, assoc=None) # note: who has `assoc`
p = Pipeline([neg, flt])
p.setups()
p


############################################################################
@patch
def delete(cls:Pipeline, idx):
    "to delete cls.tfms[idx]"
    del(cls.tfms[idx])

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3, assoc=Item)
flt = floattfm(is_tuple=True, mask=[True]*3, assoc=None) # note: who has `assoc`
p = Pipeline([neg, flt])
p.setups()
p.tfms
p.delete(0)
p.tfms


############################################################################
@patch
def remove(cls:Pipeline, tfm):
    "to remove a particular tfm from self.tfms"
    cls.tfms.remove(tfm)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3, assoc=Item)
flt = floattfm(is_tuple=True, mask=[True]*3, assoc=None) # note: who has `assoc`
p = Pipeline([neg, flt])
p.setups()
p.tfms
p.remove(neg)
p.tfms

############################################################################
@patch
def set_tupled(cls:Pipeline, m=True):
    """
    Note: run it before `cls.setups()`, due to `cls._tfms`
    "to set all tfms 'is_tuple' True"
    """
    _set_tupled(cls._tfms, m)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(mask=[True]*3, assoc=Item)
flt = floattfm(mask=[True]*3, assoc=None) # note: who has `assoc`
p = Pipeline([neg, flt])
p._tfms[0].is_tuple
p._tfms[1].is_tuple
p.set_tupled()
p._tfms[0].is_tuple
p._tfms[1].is_tuple
