from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

###############################################################################
###############################################################################
# python default `sorted` is good
t = [1,2,3]
hasattr(t, 'sorted')
sorted(t, reverse=True)
t = L(1,2,3)
hasattr(t, 'sorted')
sorted(t, reverse=True)
t = L('1','2','3')
sorted(t, reverse=True)
t = L('a','b','c')
sorted(t, reverse=True)
###############################################################################

@patch
def sortedL(cls:L, key=None, reverse=False):
    """
    "New `L` sorted by `key`. If key is str then use `attrgetter`. If key is int then use `itemgetter`."
    purpose:
    1. we want to sort more complex L such as a L of transforms
    2. different transforms have different values for property `order`
    3. we want to use the values of `order` to sort L of transforms
    """
    if isinstance(key,str):   k=lambda o:getattr(o,key,0)
    elif isinstance(key,int): k=itemgetter(key)
    else: k=key
    return L(sorted(cls.items, key=k, reverse=reverse))
###############################################################################
class _Tfm():
    def __init__(self, order=None, items=None):
        self.order = order
t1=_Tfm(1)
t1.order
t2=_Tfm(2)
t2.order
L(t2,t1)
sortedL(L(t1,t2), key='order', reverse=False)

###############################################################################
###############################################################################
list(map(str, [1,2,3]))
list(map(str, L(1,2,3)))
L(map(str, L(1,2,3))).items
###############################################################################
@patch
def mapped(cls:L, f):
    """
    purpose:
    1. we want to create a `map(f, x)` for `L`
    2. we can just call `t.mapped(f)` to transform every item of `t` by `f`
    3. in the end, we wrap a L instance onto the transformations of the `f`
    """
    return L(map(f, cls))
###############################################################################
t = L(1,2,3)
t.mapped(str)

###############################################################################
###############################################################################
z = zip([1,2,3], ['a','b', 'c'])
set(z)
z = zip([1,2,3], ['a','b', 'c'])
L(z)
# L and zip don't work well
t = L([[1,2,3], ['a','b', 'c']]); t
L(zip(t))
###############################################################################
@patch
def zipped(cls:L):
    """
    purpose:
    1. we want to zip to work directly on L just like zip on list
    2. also we want to the zip outcome to reprent easily without `set`
    """
    return L(zip(*cls))
###############################################################################
t = L([[1,2,3],'abc']); t
t.zipped()
t = L([[1,2,3], ['a', 'b', 'c']]); t
t.zipped()


###############################################################################
###############################################################################
@patch
def itemgot(cls:L, idx):
    """
    purpose:
    1. I don't believe list has such feature below
    2. if L has two lists within and we want to access the second item of both
    3. how can we do it easily?
    """
    return cls.mapped(itemgetter(idx))
###############################################################################
t = L([[1,2,3],[4,5,6]]); t
t.itemgot(1)

###############################################################################
###############################################################################
@patch
def attrgot(cls:L, k):
    """
    purpose:
    1. we may have a complex L which contains multiple class objects with
        different attributes
    2. we certainly want to extract a particular attribute of all the objects
        in L
    3. we would like to put all these attribute values into another L instance
    """
    return cls.mapped(lambda o:getattr(o,k,0))
###############################################################################
class _Tfm():
    def __init__(self, order=None, items=None):
        self.order = order
t1=_Tfm(1)
t1.order
t2=_Tfm(2)
t2.order
hasattr(t1, 'order')
t = L(t1, t2)
t.attrgot('order')
attrgot(t, 'order')

###############################################################################
###############################################################################
@patch
def tensored(cls:L):     return cls.mapped(tensor)
###############################################################################
t=L(1,2,3)
t.tensored()


###############################################################################
###############################################################################
@patch
def stack(cls:L, dim=0):
    """
    purpose:
    1. we want to easily turn a list of list into 2D tensors
    2. even easily do `T()` on them
    """
    return torch.stack(list(cls.tensored()), dim=dim)
###############################################################################
L(1,2,3).tensored()
L(1,2,3).stack(dim=0)
L(1,2,3).stack(dim=-1)
t = L(([1,2],[3,4],[5,6]))
t.tensored()
t.stack(dim=0)
t.stack(dim=-1)


###############################################################################
###############################################################################
@patch
def cat  (cls:L, dim=0):
    return torch.cat  (list(cls.tensored()), dim=dim)
###############################################################################
L([[1,2],[3,4]])
L([[1,2],[3,4]]).tensored()
L([[1,2],[3,4]]).stack(dim=0)
L([[1,2],[3,4]]).stack(dim=1)
L([[1,2],[3,4]]).cat(dim=0)
L([[1,2],[3,4]]).cat(dim=-1)

###############################################################################
add_docs(L,
         mapped="Create new `L` with `f` applied to all `items`",
         zipped="Create new `L` with `zip(*items)`",
         itemgot="Create new `L` with item `idx` of all `items`",
         attrgot="Create new `L` with attr `k` of all `items`",
         tensored="`mapped(tensor)`",
         stack="Same as `torch.stack`",
         cat="Same as `torch.cat`")
