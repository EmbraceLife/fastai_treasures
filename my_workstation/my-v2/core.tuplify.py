from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L, tensor

############
# tuplify(o, use_list=False, match=None) =>
    # = turn a L object into a tuple
    # = use_list to split a single tensor into a tuple of 3 tensors


def tuplify(o, use_list=False, match=None):
    """
    why tuplify(...):
    1. sometimes, we want to turn everything into a tuple
        so, we want to turn an object 'o' into L, and then a tuple
    2. we can shorten it by refactor into `tuplify(o)`
    3. the output is a tuple which has nothing to do with L any more
    4. it seems before we turn an object to tuple,
        we should always turn it to L first.
    """
    return tuple(L(o, use_list=use_list, match=match))

L(None)
tuplify(None, use_list=False, match=None)
t = L([1,2,3]); t
t = tuplify(t, use_list=False, match=None);t
t = tuplify(t, use_list=True, match=None);t
t = tuplify([1], use_list=True, match=[1,2,3]);t
