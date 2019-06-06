from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test, equals


###################
# test_eq = test with equals on a and b
# a, b = list, map(int, list), tensor, array, list(array)
# output = nothing, if true
# output = cname, a, b, if false

def test_eq(a,b):
    "`test` that `a==b`"
    test(a,b,equals, '==')

def examples():
    test_eq([1,2],[1,2])
    test_eq([1,2],map(int,[1,2]))
    test_eq(torch.tensor(1),1)
    test_eq(1,torch.tensor(1))
    test_eq(torch.tensor([1,2]),torch.tensor([1,2]))
    test_eq(array([1,2]),array([1,2]))
    test_eq([array([1,2]),3],[array([1,2]),3])

def inspection():
    sig(equals)
    source(equals)
    sig(test)
    source(test)
