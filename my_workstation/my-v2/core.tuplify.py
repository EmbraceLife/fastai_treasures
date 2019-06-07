from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L, tensor

############
# tuplify(o, use_list=False, match=None) =>
    # = turn a L object into a tuple
    # = use_list to split a single tensor into a tuple of 3 tensors


def tuplify(o, use_list=False, match=None):
    "Make `o` a tuple"
    return tuple(L(o, use_list=use_list, match=match))

def examples():
    test_eq(tuplify(None),())
    test_eq(tuplify([1,2,3]),(1,2,3))
    test_eq(tuplify(1,match=[1,2,3]),(1,1,1))

    test_eq(tuplify(tensor(1,2,3), use_list=True, match=None), (tensor(1), tensor(2), tensor(3)))
