from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
###################
from local.data.pipeline import Transform, Item

def _set_tupled(tfms, m=True):
    "to set all tfms `is_tuple` True"
    tfms = L(tfms)
    for t in tfms: getattr(t,'set_tupled',noop)(m)
    return tfms

@newchk
class Pipeline(Transform):
    def __init__(self, tfms=None):
        """
        steps:
        1. create an empty list for `self.tfms`
        2. make `tfms` an object of `L` and make them instances of `Transform` and assign to `self._tfms`
        """
        self.tfms,self._tfms = [],L(tfms).mapped(Transform.create)

    def setups(self, items=None):
        """
        steps:
        1. assign `self._tfms` to `tfms`
        2. assign `None` to `self._tfms`
        3. use `self.add` to add `items` to `tfms`
        """
        tfms,self._tfms = self._tfms,None
        self.add(tfms, items)

    def add(self, tfms, items=None):
        """
        steps: see it in action help clear the mind
        1. set `prev` None
        2. loop through `tfms` based on their orders
            3. add each `tfm` onto `self.tfms`
            4. if each `tfm` has attr `setup`, then call `setups(items)`
            4. meaning add `items` onto each `tfm`
        """
        prev=None
        for t in sorted(L(tfms), key=lambda o: getattr(o, 'order', 0)):
            if prev: t.prev=prev
            prev=t
            self.tfms.append(t)
            if hasattr(t, 'setup'): t.setup(items) # Transform.setup

    def composed(self, x, rev=False, fname='__call__', **kwargs):
        """
        "Compose `{fname}` of all `self.tfms` (reversed if `rev`) on `x`"
        steps:
        1. make sure `self._tfms` avaliable
        2. keep order or reverse order of `self.tfms`
        3. loop each `tfm`, to apply `tfm` onto `x`
            3. by x = `tfm.fname(x, **kwargs)` or do nothing with `noop`
        4. return `x` (which is transformed by all `tfms`)
        """

        assert not self._tfms, "Run `setup` before calling `Pipeline`"
        tfms = reversed(self.tfms) if rev else self.tfms
        for f in tfms: x = opt_call(f, fname, x, **kwargs)
        return x

    def __call__(self, x, **kwargs):
        "`__call__(x)` is to execute `composed(x)`"
        return self.composed(x, **kwargs)

    def __getitem__(self, x):
        "to `self[x]` is to `self(x)`"
        return self(x)

    def decode(self, x, **kwargs):
        "self.decode(x) => self.composed(x, rev=T, fname='decode')"
        return self.composed(x, rev=True, fname='decode', **kwargs)

    def decode_at(self, idx):
        "decode + [idx], but not figured out use [idx] usage yet"
        return self.decode(self[idx])

    def show_at(self, idx):
        "show + [idx]"
        return self.show(self[idx])

    def __repr__(self):
        "to print out all tfms"
        return str(self.tfms)

    def delete(self, idx):
        "to delete self.tfms[idx]"
        del(self.tfms[idx])

    def remove(self, tfm):
        "to remove a particular tfm from self.tfms"
        self.tfms.remove(tfm)

    def show(self, o, *args, **kwargs):
        "decode all the way/all the tfms back, and show the result"
        return self.tfms[-1].show(o, *args, **kwargs)

    def set_tupled(self, m=True):
        "to set all tfms 'is_tuple' True"
        _set_tupled(self._tfms, m)
# %%
add_docs(Pipeline,
         "A pipeline of composed (for encode/decode) transforms, setup one at a time",
         __call__="Compose `__call__` of all `tfms` on `x`",
         decode="Compose `decode` of all `tfms` on `x`",
         decode_at="Decoded item at `idx`",
         show_at="Show item at `idx`",
         show="Show item",
         delete="Delete transform `idx` from pipeline",
         remove="Remove `tfm` from pipeline",
         set_tupled="Set any `MappedTransform`s in `tfms` to tupled mode")
# %% markdown
# A list of transforms are often applied in a particular order,
# and decoded by applying in the reverse order.
# `Pipeline` provides this functionality,
# and also ensures that any `setup` methods are called,
# without including later transforms in those calls.
# NB: `setup` must be run before encoding/decoding.

pipe = Pipeline(); pipe # no tfms applied, so it will do nothing to `x`
pipe.setup() # must run before encode or decode, to reorder tfms
pipe(1) # to encode on 1 through all tfms

negtfm = lambda: Transform(operator.neg, decodes=operator.neg)
floattfm = lambda: Transform(float,decodes=int,assoc=Item)
pipe = Pipeline([negtfm(),floattfm()]); pipe
pipe.setup() # move tfms in `self._tfms` into `self.tfms` with order

start = 2
t = pipe(2); t # apply neg to 2, then apply float to -2
pipe[2] # is exactly pipe(2)
pipe.decode(t) # pipe.composed(t, rev=True, fname='decode')
pipe.decode_at(2) # ==pipe.decode(pipe[2])
pipe.show(t) # tfms[-1].show => int + print
pipe.show_at(2) # 1. t = pipe[2]; 2. pipe.show(t); 3. float.show => int + print
source(pipe.show)# very similar effect to `pipe.decode`
source(pipe.decode)
source(pipe.decode_at)# very similar effect to `pipe.show_at`
source(pipe.show_at)
# Check opposite order
pipe = Pipeline([floattfm(),negtfm()])
pipe.setup()
t = pipe(2);t # __call__
pipe.decode(t) # decode => composed on all
pipe.show(t);
pipe.show_at(t)
pipe.show(pipe[-2.0])
