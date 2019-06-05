from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import newchk, GetAttr, add_docs, coll_repr, tensor
from local.core import _listify, _mask2idxs, is_iter
# from local.core import *

Tensor.ndim = property(lambda x: x.dim())

def _mask2idxs(mask):
    mask = list(mask)
    if isinstance(mask[0],bool): return [i for i,m in enumerate(mask) if m]
    return [int(i) for i in mask]

mask = (3,)
mask = (3,5)
_mask2idxs(mask)


# to make sure L(instance_L) returns the same instance
@newchk
class L(GetAttr):
    "Behaves like a list of `items` but can also index with list of indices or masks"
    _xtra =  [o for o in dir(list) if not o.startswith('_')]

    # get items into a list and assigned to self.items and self.default
    # use_list?
    # match: match the length of items
    def __init__(self, items=None, *rest, use_list=False, match=None):
        items = [] if items is None else items
        self.items = self.default = list(items) if use_list else _listify(items)
        self.items += list(rest)
        if match is not None:
            if len(self.items)==1: self.items = self.items*len(match)
            else: assert len(self.items)==len(match), 'Match length mismatch'

    def __len__(self): return len(self.items)
    def __delitem__(self, i): del(self.items[i])
    def __repr__(self): return f'{coll_repr(self)}'
    def __eq__(self,b): return all_equal(b,self)
    def __iter__(self): return (self[i] for i in range(len(self)))
    def __mul__ (a,b): return L(a.items*b)
    def __add__ (a,b): return L(a.items+_listify(b))
    def __radd__(a,b): return L(b)+a
    def __addi__(a,b):
        a.items += list(b)
        return a


    def __getitem__(self, idx):
        "Retrieve `idx` (can be list of indices, or mask, or int) items"
        # return individual values or L instance

        ############### official and compact
        # res = [self.items[i] for i in _mask2idxs(idx)] if is_iter(idx) else self.items[idx]

        ################## made_uncool
        res = None
        if is_iter(idx):
            res = []
            for i in _mask2idxs(idx):
                res.append(self.items[i])
        else:
            res = self.items[idx]

        if isinstance(res,(tuple,list)) and not isinstance(res,L): res = L(res)
        return res

    def __setitem__(self, idx, o):
        "Set `idx` (can be list of indices, or mask, or int) items to `o` (which is broadcast if not iterable)"

        ##################
        # official compact
        # idx = idx if isinstance(idx,L) else _listify(idx)
        # if not is_iter(o): o = [o]*len(idx)
        # for i,o_ in zip(idx,o): self.items[i] = o_
        #################
        # made_uncool
        if isinstance(idx,L):
            idx = idx
        else:
            idx = _listify(idx)

        if not is_iter(o):
            o = [o]*len(idx)

        for i,o_ in zip(idx,o):
            self.items[i] = o_

    def sorted(self, key=None, reverse=False):
        "New `L` sorted by `key`. If key is str then use `attrgetter`. If key is int then use `itemgetter`."
        if isinstance(key,str):   k=lambda o:getattr(o,key,0)
        elif isinstance(key,int): k=itemgetter(key)
        else: k=key
        return L(sorted(self.items, key=k, reverse=reverse))

    def mapped(self, f):    return L(map(f, self))
    def zipped(self):       return L(zip(*self))
    def itemgot(self, idx): return self.mapped(itemgetter(idx))
    def attrgot(self, k):   return self.mapped(lambda o:getattr(o,k,0))
    def tensored(self):     return self.mapped(tensor)
    def stack(self, dim=0): return torch.stack(list(self.tensored()), dim=dim)
    def cat  (self, dim=0): return torch.cat  (list(self.tensored()), dim=dim)

add_docs(L,
         mapped="Create new `L` with `f` applied to all `items`",
         zipped="Create new `L` with `zip(*items)`",
         itemgot="Create new `L` with item `idx` of all `items`",
         attrgot="Create new `L` with attr `k` of all `items`",
         tensored="`mapped(tensor)`",
         stack="Same as `torch.stack`",
         cat="Same as `torch.cat`")

####################
# You can create an `L` from an existing iterable (e.g. a list, range, etc)
# and access or modify it with an int list/tuple index, mask, int, or slice.
# All `list` methods can also be used with `L`.

####################
# to pdb
t = L(range(12))
# run the wrapper class @newchk
# and then run the old_init L.__init__
t
list(range(12))

t.reverse()
# 1. GetAttr.__getattr__:
    # used t.__getattr__ inherited from GetAttr to extract the method `reverse`
    # t.reverse == t.__getattr__('reverse')
t.__getattr__('reverse')

t.__dir__()
# 1. GetAttr.__dir__: print out all dr, dt and _xtra together

t[0]
# L.__getitem__(idx) only return a single value
t[3]
t[3,5]
# t.__getitem__(idx) to retrieve items
    # idx can be an int, mask or list
    # it returns a new L instance
L(t)
# @newchk make sure t is return as it is, rather than creating anything new
t[3] = "h"
t[3,5] = ("j","k")
# L.__setitem__
    # to assign a single value or list to L instance

##############
# to notebook
# test_ne(t.reverse(), list(range(11)))
# test_eq(t[0], 11)
# t[3] = "h"
# test_eq(t[3], "h")
# t[3,5] = ("j","k")
# test_eq(t[3,5], ["j","k"])
# test_eq(t, L(t))
# t

####################
# You can also modify an `L` with `append`, `+`, and `*`.

# to pdb
t = L()
t.append(1)
# L._xtra
    # take all `list` methods on board for L to use
# GetAttr.__getattr__('append')
    # allow L to use `append` from list through _xtra
t

t += [3,2]
#  def __add__ (a,b): return L(a.items+_listify(b))

t = t + [4]
# def __add__ (a,b): return L(a.items+_listify(b))

t = 5 + t
# def __radd__(a,b): return L(b)+a
    # turn 5 to L(5), and then two L instance add together

L(1,2,3)
t = L(1)*5
# @newchk to initialize a L instance, L(1)
# def __mul__ (a,b): return L(a.items*b)

t = t.mapped(operator.neg)
# def mapped(self, f):    return L(map(f, self))


#######################
# to notebook
# test_eq(t, [])
# t.append(1)
# test_eq(t, [1])
# t += [3,2]
# test_eq(t, [1,3,2])
# t = t + [4]
# test_eq(t, [1,3,2,4])
# t = 5 + t
# test_eq(t, [5,1,3,2,4])
# test_eq(L(1,2,3), [1,2,3])
# test_eq(L(1,2,3), L(1,2,3))
# t = L(1)*5
# t = t.mapped(operator.neg)
# test_eq(t,[-1]*5)


#########################
# An `L` can be constructed from anything iterable,
# although tensors and arrays will not be iterated over on construction,
# unless you pass `use_list` to the constructor.

# to pdb
L([1,2,3])
L([1,2,3]).items
L(L([1,2,3]))
L('abc') # a string will be a single item
L('abc').items
L(range(0,3)) # _listify(range(0,3)) make it a list
L(o for o in range(0,3)) # _listify(a_generator) make it a list
L(tensor(0)) # a tensor is a single item
L([tensor(0),tensor(1)]) # two tensors in a list make it two items
L(tensor([0.,1.1])) # a single item tensor with two values inside
L(tensor([0.,1.1]), use_list=True)
# list(tensor([0.,1.1])) make it two separate tensors
# make a tensor with two values into two items

############################
# to notebook
# test_eq(L([1,2,3]),[1,2,3])
# test_eq(L(L([1,2,3])),[1,2,3])
# test_ne(L([1,2,3]),[1,2,])
# test_eq(L('abc'),['abc'])
# test_eq(L(range(0,3)),[0,1,2])
# test_eq(L(o for o in range(0,3)),[0,1,2])
# test_eq(L(tensor(0)),[tensor(0)])
# test_eq(L([tensor(0),tensor(1)]),[tensor(0),tensor(1)])
# test_eq(L(tensor([0.,1.1]))[0],tensor([0.,1.1]))
# test_eq(L(tensor([0.,1.1]), use_list=True), [0.,1.1])  # `use_list=True` to unwrap arrays/tensors

##########################
# If `match` is not `None` then t
    # - If `len(items)==1` then `items` is replicated,
    # - Otherwise an error is raised if `match` and `items` are not already the same size.

# to pdb
L(1,match=[1,2,3])
L([1,2],match=[2,3])
L([2],match=[1,2,3,9])

# to notebook
# test_eq(L(1,match=[1,2,3]),[1,1,1])
# test_eq(L([1,2],match=[2,3]),[1,2])
# test_fail(lambda: L([1,2],match=[1,2,3]))

#######################
show_doc(L.__getitem__)

# to pdb
t = L(range(12))
t[1,2]                # implicit tuple
t[[1,2]]              # list
t[:3]               # slice
t[[False]*11 + [True]] # mask is to use True and False list to get item
t[tensor(3)] # a tensor can be used to get item too

# to notebook
# t = L(range(12))
# test_eq(t[1,2], [1,2])                # implicit tuple
# test_eq(t[[1,2]], [1,2])              # list
# test_eq(t[:3], [0,1,2])               # slice
# test_eq(t[[False]*11 + [True]], [11]) # mask
# test_eq(t[tensor(3)], 3)

###########################
show_doc(L.__setitem__)

# to pdb
t[4,6] = 0
t[4,6]
t[4,6] = [1,2]
t[4,6]

# to notebook
# t[4,6] = 0
# test_eq(t[4,6], [0,0])
# t[4,6] = [1,2]
# test_eq(t[4,6], [1,2])

###########################
show_doc(L.mapped)
# to pdb
L(range(4)).mapped(operator.neg)

# to notebook
# test_eq(L(range(4)).mapped(operator.neg), [0,-1,-2,-3])

###########################
show_doc(L.zipped)

# to pdb
t = L([[1,2,3],'abc'])
t.zipped()

# to notebook
# t = L([[1,2,3],'abc'])
# test_eq(t.zipped(), [(1, 'a'),(2, 'b'),(3, 'c')])

############################
show_doc(L.itemgot)

# to pdb
t.itemgot(1)

# to notebook
# test_eq(t.itemgot(1), [2,'b'])

#######################
show_doc(L.attrgot)

# to pdb
a = [SimpleNamespace(a=3,b=4),SimpleNamespace(a=1,b=2)]
L(a).attrgot('b')

# to notebook
# a = [SimpleNamespace(a=3,b=4),SimpleNamespace(a=1,b=2)]
# test_eq(L(a).attrgot('b'), [4,2])

###########################
show_doc(L.sorted)
# to pdb
L(a)
L(a).sorted('a')
L(a).sorted('a').attrgot('b')

# to notebook
# test_eq(L(a).sorted('a').attrgot('b'), [2,4])

#############################
#### Tensor methods
# There are shortcuts for `torch.stack` and `torch.cat` if your `L` contains
# tensors or something convertible. You can manually convert with `tensored`.

# pdb
t = L(([1,2],[3,4]))
t.tensored()
t.stack()
t.cat()

# nb
# t = L(([1,2],[3,4]))
# test_eq(t.tensored(), [tensor(1,2),tensor(3,4)])
# test_eq(t.stack(), tensor([[1,2],[3,4]]))
# test_eq(t.cat(), tensor([1,2,3,4]))
