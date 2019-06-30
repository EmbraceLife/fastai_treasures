from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *
######################
# `replicate(item,match)`
# > copy `item` `match` times into a tuple
# > `item` = single value, list or tuple

show_doc(replicate)

def replicate(item,match):
    """
    why replcate(...)
    1. sometimes, we just want to make copies of an object,
        scalar, tuple, list, whatever;
    2. we want to control how many times to copy
    3. the number of copies == len(match)
    4. all copies are put into a tuple
    """
    return (item,)*len(match)

match = [1,1]
item = [1,2]
test_eq(replicate([1,2], t),([1,2],[1,2]))
test_eq(replicate(1, t),(1,1))
test_eq(replicate((1,2), t),((1, 2), (1, 2)))

