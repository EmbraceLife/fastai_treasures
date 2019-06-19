from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
###############################################################
from local.data.pipeline import Transform, Pipeline, Item, TfmdList, _set_tupled

###############################################################
class TfmOver(Transform):
    """
    "Create tuple containing each of `tfms` applied to each of `o`"

    purpose:
    - why do we need `TfmOver` after `Pipeline`, `TfmdList`?
    0. sometimes, we want multiple pipelines to work together
    1. therefore, we want to store multiple pipelines together
    2. we want to present the effect of different pipelines
    """
    def __init__(self, tfms=None):
        """
        oneliner:
        - TfmOver.__init__ is to create and store a list of pipelines as its `tfms`

        purpose:
        - what should be inside `TfmOver`?
            1. if you don't provide `tfms`, then this func will provide `tfms=[None]`
            2. it also provides `self.activ = None`
            3. finally get the pipeline ready by
                - `self.tfms = L(tfms).mapped(Pipeline)`
        """
        if tfms is None: tfms = [None]
        self.activ,self.tfms = None,L(tfms).mapped(Pipeline)

    @property
    def assoc(self): return self.tfms.attrgot('assoc')

    @classmethod
    def piped(cls, tfms=None, final_tfms=None):
        "`Pipeline` that duplicates input, then maps `TfmOver` over `tfms`, optionally followed by any `final_tfms`"
        tfms = L(ifnone(tfms,[None]))
        init_tfm = partial(replicate,match=tfms)
        return Pipeline([init_tfm,cls(tfms)] + _set_tupled(final_tfms))

    xt,yt = add_props(lambda i,x:x.tfms[i])

tp = TfmOver(tfms=[operator.neg, float])
tp.activ
tp.tfms # not setup yet
# tp.setups()
# tp.tfms
###############################################################
@patch
def setups(cls:TfmOver, o=None):
    """
    oneliner:
    - "Setup each of `tfms` independently"

    purpose:
    - setup is a must
    """
    for i,tfm in enumerate(cls.tfms):
        cls.activ = i
        tfm.setup(o)
    cls.activ=None

tp = TfmOver(tfms=[[operator.neg, float]])
tp.activ
tp.tfms
tp.tfms[0]._tfms[1].prev
tp.setups()
tp.tfms
isinstance(tp.tfms[0], Pipeline)
tp.tfms[0]
tp.tfms[0].tfms[1].prev
###############################################################
@patch
def __call__(cls:TfmOver, o, *args, **kwargs):
    """
    oneliner:
    - "List of output of each of `tfms` on `o`"

    purpose:
    - we do __call__ to create the effect of each pipeline on data `o`
        1. when `cls.active` is None, we apply each pipeline to each item of `o`
        1. Note: we have two pipelines, and two elements in `o`, for x, and y
        2. when `cls.active` is 0 for example, we apply the first pipeline to the first itme of `o`
    """
    if cls.activ is not None: return cls.tfms[cls.activ](o[cls.activ], *args, **kwargs)
    return [t(p, *args, **kwargs) for p,t in zip(o,cls.tfms)]

tp = TfmOver(tfms=[[operator.neg, float], [operator.neg]])
tp.setups()
tp([3,3])

###############################################################
@patch
def show(cls:TfmOver, o, ctx=None, **kwargs):
    """
    purpose:
    - we also need to see all pipelines' decoding and display original states
    - just like apply each pipeline to each item in `o`, Here
    - we decode and display each pipeline for each item in `o`

    Note:
    - to `show`, we need both `encodes` and `decodes`
    - also we need the very first tfm to have `assoc`
    """
    for p,t in zip(o,cls.tfms): ctx = t.show(p, ctx=ctx, **kwargs)
    return ctx

negtfm = Transform(operator.neg,decodes = operator.neg, assoc=Item)
fltfm = Transform(float, decodes=int)
tp = TfmOver(tfms=[[negtfm, fltfm], [negtfm]])
tp.setups()
t = tp([3,3]); t
tp.tfms
tp.show(t) # always use pdb to see the inner working


###############################################################
@patch
def decode(cls:TfmOver, o, **kwargs):
    """
    purpose:
    - match each item of `o` with each pipeline in `cls.tfms`
    - let each pipeline decode each item
    """
    return [t.decode(p, **kwargs) for p,t in zip(o,cls.tfms)]

negtfm = Transform(operator.neg,decodes = operator.neg)#, assoc=Item)
fltfm = Transform(float, decodes=int)
tp = TfmOver(tfms=[[negtfm, fltfm], [negtfm]])
tp.setups()
t = tp([3,3]); t
tp.show(t)
tp.decode(t) # always use pdb to see the inner working


###############################################################
@patch
def __repr__(cls:TfmOver):
    """
    purpose:
    - when printing `TfmOver`, we just want to see all the pipelines
    - Note: always `setups()` first
    """
    return f'TfmOver({cls.tfms})'

negtfm = Transform(operator.neg,decodes = operator.neg)#, assoc=Item)
fltfm = Transform(float, decodes=int)
tp = TfmOver(tfms=[[negtfm, fltfm], [negtfm]])
tp.setups()
tp

###############################################################
# @property
# def assoc(self): return self.tfms.attrgot('assoc')

negtfm = Transform(operator.neg,decodes = operator.neg, assoc=Item)
fltfm = Transform(float, decodes=int)
tp = TfmOver(tfms=[[negtfm, fltfm], [negtfm]])
tp.setups()
tp.assoc
##############################
# important!
# xt,yt = add_props(lambda i,x:x.tfms[i])
tp.xt
tp.yt

###############################################################
# @classmethod
# def piped(cls, tfms=None, final_tfms=None):
#     "`Pipeline` that duplicates input, then maps `TfmOver` over `tfms`, optionally followed by any `final_tfms`"
#     tfms = L(ifnone(tfms,[None]))
#     init_tfm = partial(replicate,match=tfms)
#     return Pipeline([init_tfm,cls(tfms)] + _set_tupled(final_tfms))

############## important! example #####################
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
class _TNorm(Transform):
    assoc=Item
    def __init__(self): self.m,self.s = 0,1
    def encodes(self, o): return (o-self.m)/self.s
    def decodes(self, o): return (o*self.s)+self.m
    def setup(self, items):
        its = tensor(items)
        self.m,self.s = its.mean(),its.std()

items = [1,2,3,4]
ps = TfmOver.piped([negtfm(), [negtfm(),_TNorm()]])
ps._tfms
tl = TfmdList(items, TfmOver.piped([negtfm(), [negtfm(),_TNorm()]]))
tl.tfm
# TfmdList: (#4) [1,2,3,4]
# tfms - [functools.partial(<function replicate at 0x1221898c8>, match=(#2) [<class 'local.core.negtfm'>,(#2) [<class 'local.core.negtfm'>,<class '__main__._TNorm'>]]), TfmOver((#2) [[<class 'local.core.negtfm'>],[<class 'local.core.negtfm'>, <class '__main__._TNorm'>]])]
tl.setup()
tl[0]
tl[3]
x,y = zip(*tl)
test_close(tensor(y).mean(), 0)
test_close(tensor(y).std(), 1)
test_eq(x, [-1,-2,-3,-4])
test_stdout(lambda:tl.show_at(1), 'tensor(-2.)')
test_eq(tl.tfm.assoc, [None,Item])
# %%
# Create a "batch"
b = list(zip(*tl)); b
bd = tl.decode_batch(b); bd

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
