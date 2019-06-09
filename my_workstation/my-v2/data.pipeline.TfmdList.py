from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import Transform, Item, Pipeline

def make_tfm(tfm):
    """
    steps
    1. if `tfm` is instance of `Pipeline`, return `tfm`
    2. if `tfm` is a list of things, return them as `Pipeline`
    3. otherwise return `tfm` as `Transform`

    """
    if isinstance(tfm,Pipeline): return tfm
    return Pipeline(tfm) if is_listy(tfm) else Transform.create(tfm)

@docs
class TfmdList(GetAttr):
    """
    purpose: A transform applied to a collection of `items`"
    """

    # need some extra methods from elsewhere (not defined in this class)
    _xtra = 'decode __call__ show'.split()

    # prepare for the create of such an instance, what are needed?
    def __init__(self, items, tfm, do_setup=True):
        # a list of `items`
        self.items = L(items)
        # a number of tfms (either are Pipeline or Transform)
        self.default = self.tfm = make_tfm(tfm)
        # do some setup
        if do_setup: self.setup()

    def __getitem__(self, i):
        """
        Transformed item(s) at `i`

        purpose:
        - often we need to access an item from TfmdList, like any list,
        - when we got it/them, we have to transform it/them as well.

        steps
        - get the items[i]
        - such item accessed may be more a scalar, then apply tfm to all of them
        - if just a scalar, just apply to it alone
        """
        its = self.items[i]
        if is_iter(i):
            return its.mapped(self.tfm)
        else:
            return self.tfm(its)

    def decode_batch(self, b, **kwargs):
        """"
        Decode `b`, a list of lists of pipeline outputs (i.e. output of a `DataLoader`)

        purpose:
        - we have done decoding tfms on a single value,
        - but what about a whole bunch of data samples

        steps:
        - put the bunch inot multiple L objects, and zip it, and wrap a L again
        - apply decode onto them with kwargs
        - finally zip them up again
        """
        transp = L(zip(*L(b)))
        return transp.mapped(partial(self.decode, **kwargs)).zipped()

    def setup(self):
        """
        purpose:
        - when doing __init__, some setup work are needed

        steps:
        - setup is really for tfm to do their own setups
        """
        getattr(self.tfm,'setup',noop)(self)

    def subset(self, idxs):
        """
        purpose:
        - when create a subset of TfmdList,
        - it is to create another but smaller TfmdList

        steps:
        - use __init__ method of course,
        - use `items[idxs]` so it is smaller, but `self.tfm` are the same
        - but no need to run setup again
        """
        return self.__class__(self.items[idxs], self.tfm, do_setup=False)

    def decode_at(self, idx):
        return self.decode(self[idx])
        
    def show_at(self, idx): return self.show(self[idx])
    def __eq__(self, b): return all_equal(self, b)
    def __len__(self): return len(self.items)
    def __iter__(self): return (self[i] for i in range_of(self))
    def __repr__(self): return f"{self.__class__.__name__}: {self.items}\ntfms - {self.tfm}"

    _docs = dict(setup="Transform setup with self",
                 decode_at="Decoded item at `idx`",
                 show_at="Show item at `idx`",
                 subset="New `TfmdList` that only includes items at `idxs`")


negtfm = lambda: Transform(operator.neg, decodes=operator.neg)
floattfm = lambda: Transform(float,decodes=int,assoc=Item)

pipe = Pipeline([negtfm(),floattfm()])
pipe.setup()

tl = TfmdList([1,2,3], pipe)
t = tl[1]
tl.decode_at(1)
tl.decode(t)
tl.show_at(2)

test_eq(t, -2.0)
test_eq(type(t), float)
test_eq(tl.decode_at(1), 2)
test_eq(tl.decode(t), 2)
test_stdout(lambda: tl.show_at(2), '-3')
tl
# %%
p2 = tl.subset([0,2])
test_eq(p2, [-1.,-3.])
# %% markdown
# Here's how we can use `TfmdList.setup` to implement a simple category list, getting labels from a mock file list:
# %%
class _Cat(Transform):
    assoc,order=Item,1
    def encodes(self, o): return self.o2i[o] if self._done_setup else o
    def decodes(self, o): return self.vocab[o]
    def setups(self, items): self.vocab,self.o2i = uniqueify(items, sort=True, bidir=True)

def _lbl(o): return o.split('_')[0]

test_fns = ['dog_0.jpg','cat_0.jpg','cat_2.jpg','cat_1.jpg','dog_1.jpg']
tcat = _Cat()
tl = TfmdList(test_fns, [tcat,_lbl])

test_eq(tcat.vocab, ['cat','dog'])
test_eq([1,0,0,0,1], tl)
test_eq(1, tl[-1])
test_eq([1,0], tl[0,1])
t = list(tl)
test_eq([1,0,0,0,1], t)
test_eq(['dog','cat','cat','cat','dog'], map(tl.decode,t))
test_stdout(lambda:tl.show_at(0), "dog")
tl
# %% markdown
# ### Methods
# %%
show_doc(TfmdList.__getitem__)
# %%
tl.decode(tl[1])
# %%
test_eq(tl.decode_at(1),'cat')
# %%
show_doc(TfmdList.show_at)
# %%
tl.show_at(1)
