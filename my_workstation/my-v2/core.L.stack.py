from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

show_doc(torch.stack)
show_doc(L.stack)
###############################################################################
###############################################################################
@patch
def stack(cls:L, dim=0):
    """
    why L.stack(dim)
    - when we have a `t` containing multiple equal length of list or tensors
    - we want to stack them up
    - Can we simply just run `t.stack(dim)`?

    how to use L.stack(dim)
    - `t`: a L contains e.g.,
        - (#3) [tensor([1, 2, 8]),tensor([3, 4, 9]),tensor([ 5,  6, 10])]
    - `dim = 0`: stack row by row
    - `dim = 1`: stack col by col
    - returns tensor, but L

    Note:
    - `t` does not have to contain tensors first
    - returns tensor, but L 
    """
    return torch.stack(list(cls.tensored()), dim=dim)
###############################################################################
t = L(([1,2,8],[3,4,9],[5,6,10]))
t.tensored()
t.stack(dim=0)
t.stack(dim=-1)
