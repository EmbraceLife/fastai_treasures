from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test, equals, nequals


def test_ne(a,b):
    """
    `test` that `a!=b`

    purpose:
    1. if you understand `test_eq`, you got this too
    """
    test(a,b,nequals,'!=')


test_ne([1,2],[1])
test_ne([1,2],[1,3])
test_ne(torch.tensor([1,2]),torch.tensor([1,1]))
test_ne(array([1,2]),array([1,1]))
test_ne([array([1,2]),3],[array([1,2])])
test_ne([3,4],torch.tensor([3]))
test_ne([3,4],torch.tensor([3,5]))
