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
        - when we say `setup`, we mean setup for `Transform`
        - not `Pipeline`

        steps:
        - check if `self.tfm` has attr `setup`
        - if yes, run it
        - if no, run `noop()`
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
        """
        purpose:
        - sometimes we want to access a particular value/subset of values
        - and then decode them to original state

        steps:
        - get self[idx]
        - encode them with tfms
        - decode them back
        """
        return self.decode(self[idx])

    def show_at(self, idx):
        """
        purpose:
        - sometimes we want to get access to partcular item/s in the list
        - and to show them in original state

        steps:
        - get the item/s with `self[idx]` which will be encoded
        - use `Transform.show` or `Pipeline.show` to show them
            - which is to decode through all the `prev` tfm
            - and then use `assoc.show` to display
        """
        return self.show(self[idx])

    def __eq__(self, b):
        """
        purpose:
        - sometimes, we want to compare `TfmdList` with each other
        - on their contents and length since they can be plural
        """
        return all_equal(self, b)

    def __len__(self):
        """
        purpose:
        - when we think of the length of the `TfmdList`
        - it should be the number of `items` we are dealing with, not `tfm`
        """
        return len(self.items)

    def __iter__(self):
        """
        purpose:
        - to make `TfmdList` object an iterator
        """
        return (self[i] for i in range_of(self))

    def __repr__(self):
        """
        purpose:
        - what should we look at when print out the `TfmdList` object?
        - we need to print out class name, `self.items`, `self.tfm`
        """
        return f"{self.__class__.__name__}: {self.items}\ntfms - {self.tfm}"

    # @docs, cls._docs together make `add_docs` automatic
    _docs = dict(setup="Transform setup with self",
                 decode_at="Decoded item at `idx`",
                 show_at="Show item at `idx`",
                 subset="New `TfmdList` that only includes items at `idxs`")

#####################
# How do we make use of `Transform`, `Pipeline`, `TfmdList` altogether
# first, we can create two tfms
negtfm = lambda: Transform(operator.neg, decodes=operator.neg)
floattfm = lambda: Transform(float,decodes=int,assoc=Item)
# second, put tfms together with a certain order to create a pipeline
pipe = Pipeline([negtfm(),floattfm()])
# third, pipe is really just a list of Transform,
# so make tfm setup for themselves, get them prepared
# but Transform.setups has to be customized for actual use
pipe.setup()
# now we can create a TfmdList by combining items with tfm
tl = TfmdList([1,2,3], pipe)
# now let's test it by accessing the second item of TfmdList
t = tl[1]; t
# try to decode it back
tl.decode(t)
# try decode_at(1) with access tl[1] and then decode it
test_eq(tl.decode_at(1), tl.decode(tl[1]))
# try show_at(2) with access tl[2], and show it
tl.show_at(2) == tl.show(tl[2])
# test the `__repr__` for print out content
tl
# we can create a new TfmdList with subset
p2 = tl.subset([0,2]); p2
# if you wonder whether test_eq actually do encoding,
# simple answer is test_eq => __iter__ => self[idx] => encoding
test_eq(p2, [-1.,-3.])

# Here's how we can use `TfmdList.setup` to implement a simple category list, getting labels from a mock file list:
# let's create a Tranform with customized setups
class _Cat(Transform):
    assoc,order=Item,1
    def encodes(self, o): return self.o2i[o] if self._done_setup else o
    def decodes(self, o): return self.vocab[o]
    # customize Transform.setups with uniqueify which works on TfmdList
    # since uniqueify makes TfmdList do __iter__,
    # so all tfm applied to items quietly
    def setups(self, items): self.vocab,self.o2i = uniqueify(items, sort=True, bidir=True)
# create another tfm as a pure func
def _lbl(o): return o.split('_')[0]

test_fns = ['dog_0.jpg','cat_0.jpg','cat_2.jpg','cat_1.jpg','dog_1.jpg']
tcat = _Cat() # instantiate the _Cat Tfm
tl = TfmdList(test_fns, [tcat,_lbl])
tcat.vocab
list(tl.__iter__())
tl[-1] # get tl.items[-1], and then apply tfm to it. see below to confirm
tl.tfm(tl.items[-1])
tl[0,1] # get tl.items[0,1], and then apply tfm to it. see below to confirm
tl.items[0,1].mapped(tl.tfm)
t = list(tl); t # __iter__ is intriggered
list(map(tl.decode,t))
tl.show_at(1) # first tl[1], then tl.show on it
tl.show(tl[1])
tl.decode_at(1)
tl.decode(tl[1])


test_eq(tcat.vocab, ['cat','dog'])
test_eq([1,0,0,0,1], tl)
test_eq(1, tl[-1])
test_eq([1,0], tl[0,1])
test_eq([1,0,0,0,1], t)
test_eq(['dog','cat','cat','cat','dog'], map(tl.decode,t))
test_stdout(lambda:tl.show_at(0), "dog")
