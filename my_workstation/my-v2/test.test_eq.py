from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test, equals

###################

def test_eq(a,b):
    """
    `test` that `a==b`

    purpose:
    1. you often `test` `a` and `b` using `equals` and name `equals` to be `==`
    2. you want to be lazy by just typing `test_eq(a, b)`
    3. so you use 2 to wrap 1
    """
    test(a,b,equals, '==')

test_eq([1,2],[1,2])
test_eq([1,2],map(int,[1,2]))
test_eq(torch.tensor(1),1)
test_eq(1,torch.tensor(1))
test_eq(torch.tensor([1,2]),torch.tensor([1,2]))
test_eq(array([1,2]),array([1,2]))
test_eq([array([1,2]),3],[array([1,2]),3])

show_doc(test)
