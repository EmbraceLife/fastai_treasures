from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

show_doc(L.cat)
###############################################################################
###############################################################################
@patch
def cat  (cls:L, dim=0):
    """
    why L.cat(dim)
    - we have a L with multiple lists or tensors inside
    - we want to concate them into a single tensor
    - we want `t.cat(dim=0)` to do it

    how to use `t.cat(dim)`?
    - `t`: a L with multiple lists or tensors inside
    - `dim`: either -1 or 0, but no real effect it seems
    """
    return torch.cat  (list(cls.tensored()), dim=dim)
###############################################################################
L([[1,2],[3,4]])
L([[1,2],[3,4]]).tensored()
L([[1,2],[3,4]]).stack(dim=0)
L([[1,2],[3,4]]).stack(dim=1)
L([[1,2],[3,4]]).cat(dim=0)
L([[1,2],[3,4]]).cat(dim=-1)

###############################################################################
