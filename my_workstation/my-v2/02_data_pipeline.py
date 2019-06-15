# %%
#default_exp data.pipeline
# %%
#export
from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
# %% markdown
# # Transforms and Pipeline
# test
# > Low-level transform pipelines
# %% markdown
# The classes here provide functionality for creating *partially reversible functions*, which we call `Transform`s. By "partially reversible" we mean that a transform can be `decode`d, creating a form suitable for display. This is not necessarily identical to the original form (e.g. a transform that changes a byte tensor to a float tensor does not recreate a byte tensor when decoded, since that may lose precision, and a float tensor can be displayed already.)
#
# Classes are also provided and for composing transforms, and mapping them over collections. The following functionality is provided:
#
# - A `Transform` can be created with `is_tuple=True`, which causes a single transform to be mapped over an input collection
# - `TfmOver` is a transform which applies multiple transforms over an input collection of the same length
# - `Pipeline` is a transform which composes transforms
# - `TfmdList` takes a collection and a transform, and provides an indexer (`__getitem__`) which dynamically applies the transform to the collection items.
# %% markdown
# ## Convenience functions
# %%
# export core
def opt_call(f, fname='__call__', *args, **kwargs):
    "Call `f.{fname}(*args, **kwargs)`, or `noop` if not defined"
    return getattr(f,fname,noop)(*args, **kwargs)
# %%
test_eq(opt_call(operator.neg, '__call__', 2), -2)
test_eq(opt_call(list, 'foobar', [2]), [2])

a=[2,1]
opt_call(list, 'sort', a)
test_eq(a, [1,2])
# %%
#export
def show_title(o, ax=None, ctx=None):
    "Set title of `ax` to `o`, or print `o` if `ax` is `None`"
    ax = ifnone(ax,ctx)
    if ax is None: print(o)
    else: ax.set_title(o)
# %% markdown
# ## Transform -
# %%
#export
class Item():
    "An item that displays text (for `Transform.assoc`)"
    def show(o, ctx=None, **kwargs):
        show_title(o, ctx, **kwargs)
        return ctx
# %%
# export
class Transform():
    order,mask,is_tuple,assoc,filt,_is_setup,_done_setup,prev = [0]+[None]*7
    def __init__(self, encodes=None, **kwargs):
        for k,v in kwargs.items(): setattr(self, k,v)
        if encodes:
            self.encodes=encodes
            self.order = getattr(encodes,'order',0)

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
    def create(cls, f, filt=None): return f if isinstance(f,Transform) else cls(encodes=f)
    def find_assoc(self): return self.assoc if self.assoc else self.prev.find_assoc() if self.prev else None
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
         find_assoc="Find `assoc` type by searching `prev` recursively",
         setup="Override `setups` for setup behavior",
         setups="Override to implement custom setup behavior")
# %% markdown
# In a transformation pipeline some steps need to be reversible - for instance, if you turn a string (such as *dog*) into an int (such as *1*) for modeling, then for display purposes you'll want to turn it back to a string again (e.g. when you have a prediction). In addition, you may wish to only run the transformation for a particular data subset, such as the training set.
#
# `Transform` provides all this functionality. `filt` is some dataset index (e.g. provided by `DataSource`), and you provide `encodes` and optional `decodes` functions for your code. You can pass `encodes` and `decodes` functions directly to the constructor for quickly creating simple transforms.
# %%
tfm = Transform(operator.neg, decodes=operator.neg)
start = 4
t = tfm(start)
test_eq(t, -4)
test_eq(t, tfm[start])
test_eq(tfm.decode(t), start)
# %% markdown
# If a `Transform` has a `prev` attr, it will be recursively searched to find an `assoc`, e.g. for using with `show`.
# %%
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
# %%
tfm1 = floattfm()
test_eq(tfm1.find_assoc(), Item)
tfm2 = negtfm()
test_eq(tfm2.find_assoc(), None)
tfm2.prev = tfm1
test_eq(tfm2.find_assoc(), Item)
t1 = tfm1(start)
t2 = tfm2(t1)
test_stdout(lambda:floattfm().show(t), '-4')
test_stdout(lambda:tfm2.show(t2), str(start))
# %% markdown
# Generally you'll subclass `Transform`, and `assoc`, `encodes` and `decodes`.
# %%
class _AddTfm(Transform):
    assoc=Item
    def encodes(self, x, a=1): return x+a
    def decodes(self, x, a=1): return x-a

addt  = _AddTfm()
start = 4
t = addt(start)
test_eq(t, 5)
test_eq(addt.decode(5), start)
# %%
addt.filt=1
test_eq(addt(start,filt=1), 5)
test_eq(addt(start,filt=0), start)
# %% markdown
# Set `is_tuple` to map the transform over a collection of inputs, applying it where `mask` is `True`. Note that `mask` defaults to `(True,False)`.
# %%
addt  = _AddTfm(is_tuple=True)
start = (1,2,3)
t = addt(start)
test_eq(t,(2,2,3))
test_eq(addt.decode(t), start)
# %%
tfm = _AddTfm(is_tuple=True, mask=(True,True))
start = (1,2)
t = tfm(start)
test_eq(t,(2,3))
test_eq(tfm.decode(t), start)
test_stdout(lambda:tfm.show(t), "(1, 2)")
# %% markdown
# ## Pipeline -
# %%
#export
def _set_tupled(tfms, m=True):
    tfms = L(tfms)
    for t in tfms: getattr(t,'set_tupled',noop)(m)
    return tfms
# %%
#export
@newchk
class Pipeline(Transform):
    def __init__(self, tfms=None): self.tfms,self._tfms = [],L(tfms).mapped(Transform.create)

    def setups(self, items=None):
        "Transform setup"
        tfms,self._tfms = self._tfms,None
        self.add(tfms, items)

    def add(self, tfms, items=None):
        "Call `setup` on all `tfms` and append them to this pipeline"
        prev=None
        for t in sorted(L(tfms), key=lambda o: getattr(o, 'order', 0)):
            if prev: t.prev=prev
            prev=t
            self.tfms.append(t)
            if hasattr(t, 'setup'): t.setup(items)

    def composed(self, x, rev=False, fname='__call__', **kwargs):
        "Compose `{fname}` of all `self.tfms` (reversed if `rev`) on `x`"
        assert not self._tfms, "Run `setup` before calling `Pipeline`"
        tfms = reversed(self.tfms) if rev else self.tfms
        for f in tfms: x = opt_call(f, fname, x, **kwargs)
        return x

    @property
    def assoc(self): return self.tfms[-1].find_assoc()
    def __call__(self, x, **kwargs): return self.composed(x, **kwargs)
    def __getitem__(self, x): return self(x)
    def decode(self, x, **kwargs): return self.composed(x, rev=True, fname='decode', **kwargs)
    def decode_at(self, idx): return self.decode(self[idx])
    def show_at(self, idx): return self.show(self[idx])
    def __repr__(self): return str(self.tfms)
    def delete(self, idx): del(self.tfms[idx])
    def remove(self, tfm): self.tfms.remove(tfm)
    def show(self, o, *args, **kwargs): return self.tfms[-1].show(o, *args, **kwargs)
    def set_tupled(self, m=True): _set_tupled(self._tfms, m)
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
# A list of transforms are often applied in a particular order, and decoded by applying in the reverse order. `Pipeline` provides this functionality, and also ensures that any `setup` methods are called, without including later transforms in those calls. NB: `setup` must be run before encoding/decoding.
#
# Here's some simple examples:
# %%
# Empty pipelines are a noop
pipe = Pipeline()
pipe.setup()
test_eq(pipe(1), 1)
# %%
# Check a standard pipeline
pipe = Pipeline([negtfm(),floattfm()])
pipe.setup()

start = 2
t = pipe(2)
test_eq(t, -2.0)
test_eq(type(t), float)
test_eq(t, pipe[2])
test_eq(pipe.decode(t), start)
# `show` is on `tfloat` so `show_at` decodes that tfm only
test_stdout(lambda:pipe.show_at(1), '-1')
test_eq(pipe.assoc, Item)
# %%
# Check opposite order
pipe = Pipeline([floattfm(),negtfm()])
pipe.setup()

t = pipe(2)
test_eq(t, -2.0)
# `show` is on `tfloat` so needs to decode negtfm first
test_stdout(lambda:pipe.show_at(1), '1')
test_eq(pipe.assoc, Item)
# %% markdown
# ### Methods
# %%
show_doc(Pipeline.__call__)
# %%
show_doc(Pipeline.decode)
# %%
show_doc(Pipeline.delete)
# %%
show_doc(Pipeline.remove)
# %%
show_doc(Pipeline.add)
# %%
show_doc(Pipeline.show_at)
# %%
show_doc(Pipeline.decode_at)
# %%
#export
def make_tfm(tfm):
    "Create a `Pipeline` (if `tfm` is listy) or a `Transform` otherwise"
    if isinstance(tfm,Pipeline): return tfm
    return Pipeline(tfm) if is_listy(tfm) else Transform.create(tfm)
# %% markdown
# ## TfmdList -
# %%
#export
@docs
class TfmdList(GetAttr):
    "A transform applied to a collection of `items`"
    _xtra = 'decode __call__ show assoc'.split()

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
        return transp.mapped(self.decode, **kwargs).zipped()

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
# %%
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
# %% markdown
# ## TfmOver -
# %%
#export
class TfmOver(Transform):
    "Create tuple containing each of `tfms` applied to each of `o`"
    def __init__(self, tfms=None):
        if tfms is None: tfms = [None]
        self.activ,self.tfms = None,L(tfms).mapped(Pipeline)

    def __call__(self, o, *args, **kwargs):
        "List of output of each of `tfms` on `o`"
        if self.activ is not None: return self.tfms[self.activ](o[self.activ], *args, **kwargs)
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

    @property
    def assoc(self): return self.tfms.attrgot('assoc')

    @classmethod
    def piped(cls, tfms=None, final_tfms=None):
        "`Pipeline` that duplicates input, then maps `TfmOver` over `tfms`, optionally followed by any `final_tfms`"
        tfms = L(ifnone(tfms,[None]))
        init_tfm = partial(replicate,match=tfms)
        return Pipeline([init_tfm,cls(tfms)] + _set_tupled(final_tfms))

    xt,yt = add_props(lambda i,x:x.tfms[i])
# %%
class _TNorm(Transform):
    assoc=Item
    def __init__(self): self.m,self.s = 0,1
    def encodes(self, o): return (o-self.m)/self.s
    def decodes(self, o): return (o*self.s)+self.m
    def setup(self, items):
        its = tensor(items)
        self.m,self.s = its.mean(),its.std()
# %%
items = [1,2,3,4]
tl = TfmdList(items, TfmOver.piped([negtfm(), [negtfm(),_TNorm()]]))
x,y = zip(*tl)
test_close(tensor(y).mean(), 0)
test_close(tensor(y).std(), 1)
test_eq(x, [-1,-2,-3,-4])
test_stdout(lambda:tl.show_at(1), 'tensor(-2.)')
test_eq(tl.tfm.assoc, [None,Item])
# %%
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
# %% markdown
# ## Export -
# %%
#hide
from local.notebook.export import notebook2script
notebook2script(all_fs=True)
# %%
