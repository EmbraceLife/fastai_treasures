from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
############

from local.core import is_listy, defaults, tensor, to_device

#################
# item_find(x, idx=0)
# > = recursively dive deeper to get the idx-th item of x
# > `x` = list of list or dict of dict
# > `idx` = int as index working for list and dict, or not int for dict's key
# > `idx` = user defined int works for the first level, lower levels controlled by default value 0

def item_find(x, idx=0):
    "Recursively takes the `idx`-th element of `x`"
    if is_listy(x): return item_find(x[idx])
    if isinstance(x,dict):
        key = list(x.keys())[idx] if isinstance(idx, int) else idx
        return item_find(x[key])
    return x

def examples():
    x = [[1,2,3], [2,3,4], [5,6,7]]
    item_find(x=x, idx=1)
    item_find(x=x, idx=2)
    item_find(x=x, idx=0)

    x = {'a': {"m":5, "n":7, "p":9}, 'b':{"m":15, "n":17, "p":19}}
    item_find(x=x, idx=0)
    item_find(x=x, idx=1)
    item_find(x=x, idx='b')

######################
# `find_device(b)` =
# > Recursively search the device of `b`
# > and `idx` is default 0 and not changeable

def find_device(b):
    "Recursively search the device of `b`."
    return item_find(b).device

def examples():

    t1,(t2,t3) = to_device([3,[tensor(3),tensor(2)]])

    test_eq(find_device(t2), defaults.device)
    test_eq(find_device([t2,t2]), defaults.device)
    test_eq(find_device({'a':t2,'b':t2}), defaults.device)
    test_eq(find_device({'a':[[t2],[t2]],'b':t2}), defaults.device)

    show_doc(to_device)
