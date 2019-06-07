from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L

###################
# `uniqueify(x, sort=False, bidir=False, start=None)`
# > = return a unique list
# > `x` = a list of values, duplicated, and not sorted
# > `sort = True` = sort the unique list
# > `bidir=True` = also return a dict where the unique list are the keys
# > `start=None` = if not None, then add `start` on to the unique list


def uniqueify(x, sort=False, bidir=False, start=None):
    "Return the unique elements in `x`, optionally `sort`-ed, optionally return the reverse correspondance."
    res = list(OrderedDict.fromkeys(x).keys())
    if start is not None: res = L(start)+res
    if sort: res.sort()
    if bidir: return res, {v:k for k,v in enumerate(res)}
    return res

def examples():

    test_eq(set(uniqueify([1,1,0,5,0,3])),{0,1,3,5})
    test_eq(uniqueify([1,1,0,5,0,3], sort=True),[0,1,3,5])
    v,o = uniqueify([1,1,0,5,0,3], bidir=True)
    uniqueify((1,2,3,4), sort=True, bidir=True, start=10)
