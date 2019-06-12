from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

######################
# `replicate(item,match)`
# > copy `item` `match` times into a tuple
# > `item` = single value, list or tuple

def replicate(item,match):
    """
    purpose:
    1. sometimes, we just want to make copies of an object,
        scalar, tuple, list, whatever;
    2. also we want to copy `len(match)` of times
    3. `replicate()` put `item` into a tuple and then copy `len(match)` times.
    """
    return (item,)*len(match)

t = [1,1]
test_eq(replicate([1,2], t),([1,2],[1,2]))
test_eq(replicate(1, t),(1,1))
test_eq(replicate((1,2), t),((1, 2), (1, 2)))
