from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
################

from local.core import item_find


def find_bs(b):
    """
    purpose:
    1. when dealing with ML/DL the actual data sample is at the lowest level
    2. it is the shape of the lowest level data sample matters
    3. the batch_size of data sample is the first value of `shape`
    4. `item_find(b).shape[0]` gets us the batch_size value
    """
    return item_find(b).shape[0]

x = torch.randn(4,5)
test_eq(find_bs(x), 4)
test_eq(find_bs([x, x]), 4)
test_eq(find_bs({'a':x,'b':x}), 4)
test_eq(find_bs({'a':[[x],[x]],'b':x}), 4)
