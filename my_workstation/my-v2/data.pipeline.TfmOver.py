from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
##################
from local.data.pipeline import Transform, Pipeline, Item, TfmdList, _set_tupled


class TfmOver(Transform):
    """
    "Create tuple containing each of `tfms` applied to each of `o`"

    purpose:
    - to store all tfms used?
    - therefore, such class is a subclass of Transform
    """
    def __init__(self, tfms=None):
        """
        purpose:
        - how do we create an instance of this TfmOver?
        - first, we need tfms of course
        - then, we can define active tfms, assoc,
        - convert normal tfms to pipeline

        steps:
        - if tfms args are None, make it a list of [None]
        - define:
            - `self.activ` = None,
            - `self.tfms` turned into pipeline
            - `self.assoc` = Item
        """
        if tfms is None: tfms = [None]
        self.activ,self.assoc = None,Item
        tfmsL = L(tfms)
        self.tfms = tfmsL.mapped(Pipeline)

    def __call__(self, o, *args, **kwargs):
        """
        "List of output of each of `tfms` on `o`"

        """
        if self.activ is not None:
            return self.tfms[self.activ](o[self.activ], *args, **kwargs)
        return [t(p, *args, **kwargs) for p,t in zip(o,self.tfms)]

    def show(self, o, ctx=None, **kwargs):
        "Show result of `show` from each of `tfms`"
        for p,t in zip(o,self.tfms): ctx = t.show(p, ctx=ctx, **kwargs)
        return ctx

    def decode(self, o, **kwargs): return [t.decode(p, **kwargs) for p,t in zip(o,self.tfms)]

    def __repr__(self): return f'TfmOver({self.tfms})'

    def setups(self, o=None):
        "Setup each of `tfms` independently"
        for i,tfm in enumerate(self.tfms):
            self.activ = i
            tfm.setup(o)
        self.activ=None

    @classmethod
    def piped(cls, tfms=None, final_tfms=None):
        "`Pipeline` that duplicates input, then maps `TfmOver` over `tfms`, optionally followed by any `final_tfms`"
        tfms = L(ifnone(tfms,[None]))
        init_tfm = partial(replicate,match=tfms)
        return Pipeline([init_tfm,cls(tfms)] + _set_tupled(final_tfms))

    xt,yt = add_props(lambda i,x:x.tfms[i])

negtfm = lambda: Transform(operator.neg, decodes=operator.neg)
floattfm = lambda: Transform(float,decodes=int,assoc=Item)

class _TNorm(Transform):
    assoc=Item
    def __init__(self): self.m,self.s = 0,1
    def encodes(self, o): return (o-self.m)/self.s
    def decodes(self, o): return (o*self.s)+self.m
    def setup(self, items):
        its = tensor(items)
        self.m,self.s = its.mean(),its.std()

items = [1,2,3,4]
to = TfmOver(tfms=negtfm())
to.setups()
to(items)
dt(to)
TfmOver.piped([negtfm(), [negtfm(),_TNorm()]])
tl = TfmdList(items, TfmOver.piped([negtfm(), [negtfm(),_TNorm()]]))

x,y = zip(*tl)
test_close(tensor(y).mean(), 0)
test_close(tensor(y).std(), 1)
test_eq(x, [-1,-2,-3,-4])
test_stdout(lambda:tl.show_at(1), 'tensor(-2.)')

# Create a "batch"
b = list(zip(*tl))
bd = tl.decode_batch(b)

test_eq(len(bd),2)
test_eq(bd[0],items)
test_eq(bd[1],items)
test_eq(type(bd[1][0]),Tensor)
print('b ',b)
print('bd',bd)
# %%
# Empty tuplify
tp = TfmOver()
tp.setup()
test_eq(tp([1]), [1])
