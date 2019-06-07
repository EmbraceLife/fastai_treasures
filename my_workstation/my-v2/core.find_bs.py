from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
################

from local.core import item_find

################
# `find_bs(b)` = Recursively search the batch size of `b`
# `b` = a batch of dataset
# batch_size = the shape[0] of first item of b recursively

def find_bs(b):
    "Recursively search the batch size of `b`."
    return item_find(b).shape[0]

def examples():
    x = torch.randn(4,5)
    test_eq(find_bs(x), 4)
    test_eq(find_bs([x, x]), 4)
    test_eq(find_bs({'a':x,'b':x}), 4)
    test_eq(find_bs({'a':[[x],[x]],'b':x}), 4)
