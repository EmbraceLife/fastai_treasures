from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
# %%
# Not exported since we only use it for examples
from PIL import Image


# ## TfmdDL -
# %%
#export
def _DataLoader__getattr(self,k):
    try: return getattr(self.dataset, k)
    except AttributeError: raise AttributeError(k) from None
DataLoader.__getattr__ = _DataLoader__getattr
# %%
#export
@docs
class TfmdDL(GetAttr):
    "Transformed `DataLoader` using a `Pipeline` of `tfm`"
    _xtra = 'batch_size num_workers dataset sampler pin_memory'.split()

    def __init__(self, dataset, tfms=None, bs=16, is_tuple=True, shuffle=False,
                 sampler=None, batch_sampler=None, num_workers=1, **kwargs):
        tfm = Pipeline(tfms)
        if is_tuple: tfm.set_tupled()
        self.dl = DataLoader(dataset, bs, shuffle, sampler, batch_sampler, num_workers=num_workers)
        self.default,self.tfm = self.dl,tfm
        for k,v in kwargs.items(): setattr(self,k,v)
        tfm.setup(self)
        if len(tfm.tfms) > 0 and hasattr(self.dataset, 'tfm'):
            tfm.tfms[0].assoc = getattr(self.dataset.tfm,'assoc',None)

    def __len__(self): return len(self.dl)
    def __iter__(self): return map(self.tfm, self.dl)
    def one_batch(self): return next(iter(self))
    def decode(self, b): return getattr(self.dataset,'decode_batch',noop)(self.tfm.decode(b))

    def show_batch(self, b=None, max_rows=1000, ctxs=None, **kwargs):
        "Show `b` (defaults to `one_batch`), a list of lists of pipeline outputs (i.e. output of a `DataLoader`)"
        if b is None: b=self.one_batch()
        b = self.tfm.decode(b)
        rows = itertools.islice(zip(*L(b)), max_rows)
        if ctxs is None: ctxs = [None] * len(b[0] if is_iter(b[0]) else b)
        for o,ctx in zip(rows,ctxs): self.dataset.show(o, ctx=ctx)

    _docs = dict(decode="Decode `b` using `ds_tfm` and `tfm`",
                 show_batch="Show each item of `b`",
                 one_batch="Grab first batch of `dl`")
# %%
tfm = Transform(torch.neg,decodes=torch.neg)
dummy_tfm = Transform(noop,assoc=Item)
start = range(50)
tl = TfmdList(start, dummy_tfm)
tdl = TfmdDL(tl, tfm, is_tuple=False, bs=4)
test_eq(start, tdl.dataset)
test_eq(len(tdl), (len(tl)-1)//4+1)
test_eq(tdl.batch_size, 4)
# %% markdown
# ### Methods
# %%
show_doc(TfmdDL.one_batch)
# %%
b = tdl.one_batch()
test_eq([0,-1,-2,-3], b)
# %%
show_doc(TfmdDL.decode)
# %%
test_eq(tdl.decode(b), [[0,1,2,3]])
# %%
show_doc(TfmdDL.show_batch)
# %%
test_stdout(tdl.show_batch(), """(tensor(0),)
(tensor(1),)
(tensor(2),)
(tensor(3),)""")
# %% markdown
