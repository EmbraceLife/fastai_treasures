from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *
from local.core import _mask2idxs

@patch
def __getitem__(cls:L, idx):
    """
    why need __getitem__?
    - We'd like to access any elements of L by its idx
    - even better, if idx is multiple, create a new L instance

    How to use __getitem__?
    - `L(1,2,3)[idx]`
    - `L(1,2,3)[0]`
    - `L(1,2,3)[1,2]`
    - if `idx` is scalar, return a scalar;
    - if `idx` is multiple, return a L object

    How does it work?
    - if `idx` is scalar, assign `cls.items[idx]` to `res`
    - if `idx` is multiple, make sure all masks turned to idxs
        - and put all selected elements into a list
        - assign the list to `res`
    - if `res` is tuple or list but not L, turn it into L
    - return `res`
    """
    res = [cls.items[i] for i in _mask2idxs(idx)] if is_iter(idx) else cls.items[idx]

    if isinstance(res,(tuple,list)) and not isinstance(res,L): res = L(res)
    return res


L(1,2,3)[0]
L(1,2,3)[1,2]
L(1)
L(1,2,3,4,5)[True, False, True]
