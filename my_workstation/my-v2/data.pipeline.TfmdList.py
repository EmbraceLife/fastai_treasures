from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import Transform, Item, Pipeline, _set_tupled
######################################################################
def make_tfm(tfm):
    """
    purpose:
    - why need `make_tfm`?
    1. we have `Transform` to create and deal a single `tfm`
    2. we have `Pipeline` to create and deal with a bunch of `tfms`
    3. but they are essentially made by the same material
    4. why not use a single func to create either of them?

    steps
    1. if `tfm` is already `Pipeline`, just return itself
    2. if `tfm` is a list of things, convert them to a `Pipeline`
    3. if `tfm` is a singular thing, just convert it to a `Transform`
    """
    if isinstance(tfm,Pipeline): return tfm
    return Pipeline(tfm) if is_listy(tfm) else Transform.create(tfm)

tfm = Pipeline(tfms=[operator.neg, float])
make_tfm(tfm)._tfms
tfm = [operator.neg, float]
make_tfm(tfm)._tfms
tfm = float
make_tfm(tfm)

######################################################################
@docs
class TfmdList(GetAttr):
    """
    purpose:
    - why need `TfmdList` given `Pipeline` also handling multiple tfms?
    1. `Pipeline` primarily creates and deals with `tfms`
    2. `TfmdList` primarily does application to `items`

    oneliner:
    - A transform applied to a collection of `items`"

    steps:
    - `@docs`
        1. to integrate docs into the class as dict
    - `GetAttr`
        1. super class to `TfmdList`
        2. borrow 3 methods `decode`, `__call__`, `show` from Pipeline or Transform
    """

    # need some extra methods from elsewhere (not defined in this class)
    _xtra = 'decode __call__ show'.split()
    # @docs, cls._docs together make `add_docs` automatic
    # _docs = dict(setup="Transform setup with self",
    #              decode_at="Decoded item at `idx`",
    #              show_at="Show item at `idx`",
    #              subset="New `TfmdList` that only includes items at `idxs`")
    _docs = {}

    # prepare for the create of such an instance, what are needed?
    def __init__(self, items, tfm, do_setup=True):
        """
        purpose:
        - what to construct?
            1. differ from Pipeline, we need to deal with `items`, so put them under management of `L`
            2. to tranform, we need either `Transform` or `Pipeline` instances
            3. why don't we do the other `setup` here too, instead of another separate step?
        """
        self.items = L(items)
        self.default = self.tfm = make_tfm(tfm)
        if do_setup: self.setup()

    def setup(self):
        """
        purpose:
        - it is asked to do `setup` on `Pipeline` and `Transform` level
        - first, `pipeline.setup` will sort `tfms` by `order`
        - and set `prev` based on the order of Transforms, also
        - get Transforms from `self._tfms` to `self.tfms`
        - second `transform.setup` will make `_is_setup`, `_done_setup` true, and nothing else
        - Note: on Pipeline and Transform level, see args `setup(TfmdList)`
        - the full process:
            `TfmdList.setup()`=> `Pipeline.setup(tfmdlist as item)` inherit without overwritten from `Transform.setup(items)` => `Pipeline.setups(items)` inherit and overwritten => `Pipeline.add(tfms, items)` to order all tfms and loop through them for each tfm setup => `Transform.setup(items)` (turn `_is_setup` and `_done_setup` True) => `Transform.setups(items)` (pass) or other overwritten funcs
        """
        getattr(self.tfm,'setup',noop)(self)

tfm = Pipeline(tfms=[operator.neg, float])
make_tfm(tfm)._tfms
t = TfmdList([1,2,3], tfm, do_setup=True)

tfm = [operator.neg, float]
make_tfm(tfm)._tfms
t = TfmdList([1,2,3], tfm, do_setup=True)

tfm = float
make_tfm(tfm)
t = TfmdList([1,2,3], tfm, do_setup=True)

######################################################################
@patch
def __getitem__(cls:TfmdList, i):
    """
    Transformed item(s) at `i`

    purpose:
    - What exactly `TfmdList.__getitem__(i)` differ from that of `Pipeline` and `Transform`?
        1. `__getitem__` from both `Pipeline` and `Transform`
            1.1 apply `tfms` to `i`
            1.2 `i` is `items` themselves which can be a scalar or multiple
            1.3 `i` is not `idx` in fact
        2. whereas in `TfmdList`, `i` is really `idx`
            2.1 `TfmdList` already has `items` embedded
            2.2 `TfmdList.items[i]`, `L.mapped`, `TfmdList.tfm` onto themselves, if `i` `is_iter`
            2.3. if `i` is scalar, just let `TfmdList.tfm` apply onto `TfmdList.items[i]`
    """
    its = cls.items[i]
    if is_iter(i):
        return its.mapped(cls.tfm)
    else:
        return cls.tfm(its)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
pipe = Pipeline([negtfm(),floattfm()])
pipe.setup() # inherit from `Transform.setup()`
tl = TfmdList([1,2,3], pipe)
tl[1]
tl[2]

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
pipe = Pipeline([negtfm(),floattfm()])
pipe.set_tupled()
pipe.setup() # inherit from `Transform.setup()`
pipe.tfms[0].is_tuple
pipe.tfms[0].mask = [True]*3
pipe.tfms[1].mask = [True]*3
tl = TfmdList([1,2,3], pipe)
tl[:]

######################################################################
@patch
def decode_batch(cls:TfmdList, b, **kwargs):
    """"
    Decode `b`, a list of lists of pipeline outputs (i.e. output of a `DataLoader`)

    purpose:
    - previously with `Pipeline.decode` we can do decode on multiple values
    - but what about a batch of datasamples with x and y?
        1. we'd like our func to eat a batch of encoded (x, y) in one piece `(L(zip(*L(b))))` ==> `L(b).zipped()`
        2. so that we may decode them in one piece
        3. and output them in one piece
    """
    transp = L(zip(*L(b)))
    return transp.mapped(partial(cls.decode, **kwargs)).zipped()

from local.data.pipeline import TfmOver #, TfmdList
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
items = [1,2,3,4]
tl = TfmdList(items, TfmOver.piped([negtfm(), floattfm()])); tl
# Create a "batch"
b = list(zip(*tl));b
transp = L(zip(*L(b))); transp
res = transp.mapped(partial(tl.decode)); res
res.zipped()
bd = tl.decode_batch(b); bd

######################################################################
@patch
def subset(cls:TfmdList, idxs):
    """
    purpose:
    - sometimes, we may want to cut a portion from a `TfmdList`
        - and make it a separate but smaller `TfmdList`
    - Therefore, we actually run `__init__` again here
        - only a subset of `self.items`
        - same `self.tfm`
        - but `do_setup` set False
    - The reason why `do_setup` False, is usually it is already setted up by running `__init__` in earlier codes
    """
    return cls.__class__(cls.items[idxs], cls.tfm, do_setup=False)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
pipe = Pipeline([negtfm(),floattfm()])
tl = TfmdList([1,2,3], pipe, do_setup=True)
tl[1]
tl[2]
tl.tfm.tfms[1].prev
tls=tl.subset([0,1])
tls.tfm.tfms[1].prev
tls.items

######################################################################
@patch
def decode_at(cls:TfmdList, idx):
    """
    purpose:
    - `Pipeline.decode_at(idx)` is to encode and decode on the value `idx` through many tfms
    - but `TfmdList.decode_at(idx)` is to encode and decode on `items[idx]` through many tfms
    - `self.decode` can either be `Pipeline.decode` or `Transform.decode`
    """
    return cls.decode(cls[idx])

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int)
pipe = Pipeline([negtfm(),floattfm()])
tl = TfmdList([1,2,3], pipe, do_setup=True)
tl.decode_at(0)
tl.decode_at(2)

######################################################################
@patch
def show_at(cls:TfmdList, idx):
    """
    purpose:
    - maybe sometimes we just want to see `items[idx]` in its original state without transformation
    - differ from `decode_at`, `show_at` uses `assoc.show` to display
        - it could be more flexible in displaying different types
    - through `GetAttr` and `_xtra`, `TfmdList` inherited `show` from `Transform`

    steps:
    1. `self[idx]` get `items[idx]` encoded
    2. `Transform.show` allows the encoded `items[idx]` to be decoded all the way back with `prev`
    3. and get displayed by `assoc.show`
    """
    return cls.show(cls[idx])

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int)
pipe = Pipeline([negtfm(),floattfm()])
tl = TfmdList([1,2,3], pipe, do_setup=True)
tl[0]
tl.show_at(0)
tl.show_at(2)

######################################################################
@patch
def __eq__(cls:TfmdList, b):
    """
    purpose:
    - sometimes, we want to compare `TfmdList` with each other
    - on their contents and length since they can be plural
    """
    return all_equal(cls, b)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int)
pipe = Pipeline([negtfm(),floattfm()])
tl1 = TfmdList([1,2,3], pipe, do_setup=True)
tl2 = TfmdList(L(1,2,3), pipe, do_setup=True)
tl1 == tl2
tl1.__eq__(tl2) # note: all iteration actions require __getitem__

######################################################################
@patch
def __len__(cls:TfmdList):
    """
    purpose:
    - when we think of the length of the `TfmdList`
    - it should be the number of `items` we are dealing with, not `tfm`
    """
    return len(cls.items)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int)
pipe = Pipeline([negtfm(),floattfm()])
tl1 = TfmdList([1,2,3], pipe, do_setup=True)
len(tl1)
tl1.__len__()

######################################################################
@patch
def __iter__(cls:TfmdList):
    """
    purpose:
    - to make `TfmdList` object an iterator
    """
    return (cls[i] for i in range_of(cls))

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int)
pipe = Pipeline([negtfm(),floattfm()])
tl = TfmdList([1,2,3], pipe, do_setup=True)
tl[0]
g = tl.__iter__()
next(g)

######################################################################
@patch
def __repr__(cls:TfmdList):
    """
    purpose:
    - what should we look at when print out the `TfmdList` object?
    - to know everything, we could print out:
        1. class name,
        2. `cls.items`,
        3. `cls.tfm`
    """
    return f"{cls.__class__.__name__}: {cls.items}\ntfms - {cls.tfm}"

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int)
pipe = Pipeline([negtfm(),floattfm()])
tl = TfmdList([1,2,3], pipe, do_setup=True)
tl

################### more complex example
class _Cat(Transform):
    assoc,order=Item,1
    def encodes(self, o): return self.o2i[o] if self._done_setup else o
    def decodes(self, o): return self.vocab[o]
    def setups(self, items): self.vocab,self.o2i = uniqueify(items, sort=True, bidir=True)

def _lbl(o): return o.split('_')[0]

test_fns = ['dog_0.jpg','cat_0.jpg','cat_2.jpg','cat_1.jpg','dog_1.jpg']
tcat = _Cat()

# important!
tl = TfmdList(test_fns, [tcat,_lbl]) # TfmdList.setup() is done
tcat.vocab
tl

# important! on __iter__, __getitem__
test_eq([1,0,0,0,1], tl) # require tl.__iter__ and require tl[idx]
list(tl.__iter__())
tl[-1]
t = list(tl);t # require tl.__iter__ and require tl[idx]

# important! on __iter__, __getitem__
list(map(tl.decode,[1, 0, 0, 0, 1]))
list(map(tl.decode,t)) # require tl.__iter__ and require tl[idx] return [1, 0, 0, 0, 1]

# important! why not get back to the very original state
tl.show_at(0) # split by "_" have no decode
test_stdout(lambda:tl.show_at(0), "dog")
tl.decode(tl[1])
tl.decode_at(1)
test_eq(tl.decode_at(1),'cat')
tl.show_at(1)
