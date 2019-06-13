from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L
#####################
# `is_listy(x)` = whether it is instance of tuple, list, L or slice

def is_listy(x):
    """
    purpose:
    1. to us to be a list like object, it can be any of the following:
    2. tuple, list, L, slice
    """
    return isinstance(x, (tuple,list,L,slice))


assert is_listy([1])
assert is_listy(L([1]))
assert is_listy(slice(2)) # when and how to use slice?
assert not is_listy(torch.tensor([[1,3],[2,4]]))
