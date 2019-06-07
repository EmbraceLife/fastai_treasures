from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

#########################
# `range_of(x)` = return a list of indexes for `x`

def range_of(x):
    "All indices of collection `x` (i.e. `list(range(len(x)))`)"
    return list(range(len(x)))

test_eq(range_of([1,1,1,1]), [0,1,2,3])
