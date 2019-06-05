from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc


Tensor.ndim = property(lambda x: x.dim())

def _mask2idxs(mask):
    mask = list(mask)
    if isinstance(mask[0],bool): return [i for i,m in enumerate(mask) if m]
    return [int(i) for i in mask]

mask = (3,)
_mask2idxs(mask)
mask = (3,5)
_mask2idxs(mask)
# mask = 3 or (3) won't work
mask = [3]
_mask2idxs(mask)
