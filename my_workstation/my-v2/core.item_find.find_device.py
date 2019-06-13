from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
############

from local.core import is_listy, defaults, tensor, to_device, L

def item_find(x, idx=0):
    """
    purpose:
    1. with `apply` we can dive deep to transform every item in all levels
    2. but what if we just want to access an item
        from the lowest/final leaf of data
    3. `idx` allows us to pick which branch/top_level of the data tree, and
    4. after top_level, `idx` remains 0, so `item_find(x, idx=0)` gives us
        the lowest/final_level leaf/item of the tree/data
        note: it is like `x[idx][0]...[0]`
    5. also, `x` can be listy(tuple, list, slice, L) or dict
    """
    if is_listy(x): return item_find(x[idx])
    if isinstance(x,dict):
        key = list(x.keys())[idx] if isinstance(idx, int) else idx
        return item_find(x[key])
    return x


x = [[1,2,3], [2,3,4], [5,6,7]]
item_find(x=x, idx=1)
x = L(([1,2,3], [2,3,4], [5,6,7]))
item_find(x=x, idx=2)
x = ((1,2,3), (2,3,4), (5,6,7))
item_find(x=x, idx=0)

x = {'a': {"m":5, "n":7, "p":9}, 'b':{"m":15, "n":17, "p":19}}
item_find(x=x, idx=0)
item_find(x=x, idx=1)
item_find(x=x, idx='b')

###############################################################################

def find_device(b):
    """
    purpose:
    1. sometimes you may want to checkout the device which the lowest/final_level tensor is on
    2. this func can give us the device of the first branch's lowest leaf of data `x`
    """
    return item_find(b).device



t1,(t2,t3) = to_device([3,[tensor(3),tensor(2)]])

test_eq(find_device(t2), defaults.device)
test_eq(find_device([t2,t2]), defaults.device)
test_eq(find_device({'a':t2,'b':t2}), defaults.device)
test_eq(find_device({'a':[[t2],[t2]],'b':t2}), defaults.device)

show_doc(to_device)
