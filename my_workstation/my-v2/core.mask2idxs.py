from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

########################
# `mask2idxs(mask)` = turn mask into a list of idx/values as L object
# `mask` = tuple, list of values, strings, bools, even a tensor of list
# `mask` = can't be single value like 3, or (3), but (3,) or [3] works

from local.core import _mask2idxs, L

def mask2idxs(mask):
    "Convert bool mask or index list to index `L`"
    return L(_mask2idxs(mask))


test_eq(mask2idxs([False,True,False,True]), [1,3])
test_eq(mask2idxs(torch.tensor([1,2,3])), [1,2,3])
mask2idxs([10, 8, 24, 0])
mask2idxs(['10', '8', '24', '0'])

mask = (3,)
_mask2idxs(mask)
mask2idxs(mask)

mask = (3,5)
_mask2idxs(mask)
mask2idxs(mask)

# mask = 3 or (3) won't work
mask = [3, 3, 5]
_mask2idxs(mask)
mask2idxs(mask)

mask = ['3', '8']
_mask2idxs(mask)
mask2idxs(mask)

mask = torch.tensor([1,2,3])
_mask2idxs(mask)
mask2idxs(mask)

mask = [True, False, True]
_mask2idxs(mask)
mask2idxs(mask)
