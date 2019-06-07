from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc


Tensor.ndim = property(lambda x: x.dim())


########################
# `_mask2idxs(mask)` = turn mask into a list of idx/values
# `mask` = tuple, list of values, strings, bools, even a tensor of list
# `mask` = can't be single value like 3, or (3), but (3,) or [3] works

def _mask2idxs(mask):
    mask = list(mask)
    if isinstance(mask[0],bool): return [i for i,m in enumerate(mask) if m]
    return [int(i) for i in mask]

mask = [9] #or (3) won't work

mask = (3,)
_mask2idxs(mask)
mask = (3,5)
_mask2idxs(mask)

mask = [3, 3, 5]
_mask2idxs(mask)

mask = ['3', '8']
_mask2idxs(mask)

mask = torch.tensor([1,2,3])
_mask2idxs(mask)

mask = [True, False, True]
_mask2idxs(mask)
