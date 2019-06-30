from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import * 

###################
# `uniqueify(x, sort=False, bidir=False, start=None)`
# > = return a unique list
# > `x` = a list of values, duplicated, and not sorted
# > `sort = True` = sort the unique list
# > `bidir=True` = also return a dict where the unique list are the keys
# > `start=None` = if not None, then add `start` on to the unique list
show_doc(uniqueify)

def uniqueify(x, sort=False, bidir=False, start=None):
    """
    why uniquefy(...):
    1. of course, we want to be able to get unique values from a long list with duplicated values
    2. also we want the freedom to add extra values to the front of the unique list
    3. also we want the flexibility for the list to be sorted
    4. even better, we want the flexibility to output the unique list with index as well.
    
    how to achieve it?
    1. `(OrderedDict.fromkeys(x).keys())` achieve step 1
    2. L.__add__ achieves step 2
    3. L.sort() -> step 3
    4. enumerate(res) -> step 4
    
    Note:
    1. x has a list-like, but values have to be numeric, Path won't do here.
    """
    res = list(OrderedDict.fromkeys(x).keys())
    if start is not None: res = L(start)+res
    if sort: res.sort()
    if bidir: return res, {v:k for k,v in enumerate(res)}
    return res

x = [1,1,0,5,0,3]
start = [9,10]
bidir = True
sort = True

##########################
# important! : not used for the following situation
x = ['dir/8/abc01.png', 'dir/4/abc02.png']
t1 = list(map(Path, x))
uniqueify(t1, sort=False, bidir=True)
OrderedDict.fromkeys(t1)
