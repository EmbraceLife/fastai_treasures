from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc


def make_tfm(tfm):
    "Create a `Pipeline` (if `tfm` is listy) or a `Transform` otherwise"
    if isinstance(tfm,Pipeline): return tfm
    return Pipeline(tfm) if is_listy(tfm) else Transform.create(tfm)

@docs
class TfmdList(GetAttr):
    "A transform applied to a collection of `items`"
    _xtra = 'decode __call__ show'.split()

    def __init__(self, items, tfm, do_setup=True):
        self.items = L(items)
        self.default = self.tfm = make_tfm(tfm)
        if do_setup: self.setup()

    def __getitem__(self, i):
        "Transformed item(s) at `i`"
        its = self.items[i]
        return its.mapped(self.tfm) if is_iter(i) else self.tfm(its)

    def decode_batch(self, b, **kwargs):
        "Decode `b`, a list of lists of pipeline outputs (i.e. output of a `DataLoader`)"
        transp = L(zip(*L(b)))
        return transp.mapped(partial(self.decode, **kwargs)).zipped()

    def setup(self): getattr(self.tfm,'setup',noop)(self)
    def subset(self, idxs): return self.__class__(self.items[idxs], self.tfm, do_setup=False)
    def decode_at(self, idx): return self.decode(self[idx])
    def show_at(self, idx): return self.show(self[idx])
    def __eq__(self, b): return all_equal(self, b)
    def __len__(self): return len(self.items)
    def __iter__(self): return (self[i] for i in range_of(self))
    def __repr__(self): return f"{self.__class__.__name__}: {self.items}\ntfms - {self.tfm}"

    _docs = dict(setup="Transform setup with self",
                 decode_at="Decoded item at `idx`",
                 show_at="Show item at `idx`",
                 subset="New `TfmdList` that only includes items at `idxs`")

pipe = Pipeline([negtfm(),floattfm()])
pipe.setup()

tl = TfmdList([1,2,3], pipe)
t = tl[1]
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
