from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

Tensor.ndim = property(lambda x: x.dim())

def _mask2idxs(mask):
    """
    purpose:
    1. we like `data[index]` where `index` can be [8, 4, 2]
    2. but can't avoid `data[mask]`, where `mask` can be:
        a. [True, False, True] or
        b. ['8', '4', '3']
    3. we would love to have a lazy func to convert mask to proper index

    steps:
    1. turn `mask` to a list
    2. if the first item of `mask` is `bool`, then
        a. enumerate the mask to spit out (index, value) one at a time
        b. if a value is True, then put the index into a list
        c. return the list
    3. if not `bool`,
        a. loop through the mask item and make them a list of integer
        b. return the list
    """
    mask = list(mask)
    if isinstance(mask[0],bool): return [i for i,m in enumerate(mask) if m]
    return [int(i) for i in mask]

mask = [True, False, True]
list(enumerate(mask))
_mask2idxs(mask)
mask = ['0', '4', '1', '9']
_mask2idxs(mask)

from local.core import L

def mask2idxs(mask):
    "Convert bool mask or index list to index `L`"
    return L(_mask2idxs(mask))

mask = [True, False, True]
list(enumerate(mask))
mask2idxs(mask)
mask = ['0', '4', '1', '9']
mask2idxs(mask)
