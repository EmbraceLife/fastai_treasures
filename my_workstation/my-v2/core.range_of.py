from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

#########################
# `range_of(x)` = return a list of indexes for `x`

def range_of(x):
    """
    purpose:
    1. sometimes, we want to create a list of idxs for a collection of objects
    2. `range_of(x)` does exactly that
    """
    return list(range(len(x)))

test_eq(range_of([1,1,1,1]), [0,1,2,3])
range_of([[1,2],[3,4],[4,5]])
