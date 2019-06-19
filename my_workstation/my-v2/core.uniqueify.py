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
    """
    purpose:
    1. sometimes, we want to find out unique values of a long duplicated list
        `list(OrderedDict.fromkeys(x).keys())` can achieve it
    2. then you may also want add values to the head of the unique list:
        you can use `L.__add__` turn the whole thing into a L object
    3. you may want to sort the list or L object or not
    4. finally, you may choose to output the list/L
        together with a dict in which keys are unique values, values are idx
    """
    res = list(OrderedDict.fromkeys(x).keys())
    if start is not None: res = L(start)+res
    if sort: res.sort()
    if bidir: return res, {v:k for k,v in enumerate(res)}
    return res

x = [1,1,0,5,0,3]
x = list(OrderedDict.fromkeys(x).keys()); x
x = L(8,9) + x
x.sort(); x
{v:k for k,v in enumerate(x)}

t = [1,1,0,5,0,3]
start = [8,9]
uniqueify(t, sort=False, bidir=True, start=start)
uniqueify(t, sort=True, bidir=True, start=start)

##########################
# important! : not used for the following situation
t = ['dir/8/abc01.png', 'dir/4/abc02.png']
t1 = list(map(Path, t))
uniqueify(t1, sort=False, bidir=True)
OrderedDict.fromkeys(t1)
