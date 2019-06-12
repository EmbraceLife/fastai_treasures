from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import newchk, GetAttr, add_docs, coll_repr, tensor
from local.core import _listify, _mask2idxs, is_iter, patch


Tensor.ndim = property(lambda x: x.dim())

@newchk
class L(GetAttr):
    """
    purpose:
    1. although with `_listify`, we can make everything a list
    2. but don't we always wish for more features for the **List** of things
    3. why don't we add more flexibilities and functionalities beyond 'list'

    What new features `@newchk` offer new features to `L`?
    1. create a new L object from values `items`
    2. if `items` is instance of `L`, return the instance

    What new features `GetAttr` offer to `L`?
    1. inherit from `GetAttr`, `L` can borrow others' methods
    2. it actually can borrow all methods from `list` with `_xtra`
    """
    _xtra =  [o for o in dir(list) if not o.startswith('_')]

    def __init__(self, items=None, *rest, use_list=False, match=None):
        """
        purpose:
        0. how do we get started to create a powerful L over list?
        1. first, we need data, i.e., `items`, with more flexibility
            a. `items` can be `None`, we turn it to `[]`. (list(None))
            b. `items` can be anything else, we turn a list with `_listify`
            c. `use_list=True`, we use `list(items)` strange behavior
                    to break it into pieces and then wrap with `[]`
        2. we add flexibility to do `L.__init__(1,2,3)` by the power of
            `self.items += list(rest)`, just like we did in `core.tensor`
        3. `match` enables `self.items` to be equal length to `match`
            or exception rise
        """
        items = [] if items is None else items
        self.items = self.default = list(items) if use_list else _listify(items)
        self.items += list(rest)
        if match is not None:
            if len(self.items)==1: self.items = self.items*len(match)
            else: assert len(self.items)==len(match), 'Match length mismatch'

###############################################################################

##### @newchk and GetAttr added new powerful features over list ############
# power 1. @newchk makes the following flexibility over `list`
t1 = L(1,2,3); t2 = L(t1)
test_eq(t1, t2)
# power 2`GetAttr` borrow everything a list has
t1.append(4); t1.items
t1.reverse(); t1.items
t1._xtra[:3]
########### __init__ added new powerful features over list ###########
# power 1.a L(None) vs list(None)
t = L(None); t.items
test_fail(lambda: list(None)) #
# power 1.b: make everything else a list even when `list()` can't
test_fail(lambda: list(tensor(3)))
t = L(tensor(3)); t.items
# power 1.c: more control over list() strange behavior
list('yes')
t = L('yes'); t.items
t = L('yes', use_list=True); t.items
list(array([1,2,3]))
t = L(array([1,2,3])); t.items
t = L(array([1,2,3]), use_list=True); t.items
t = L(array([1.,2]), use_list=True); t.items
list(tensor(1,2))
t = L(tensor(1,2), use_list=True); t.items
# power 2: to do free style `L(1,2,3)` where `list` can't
test_fail(lambda: list(1,2,3))
t = L(1,2,3); t.items
# power 3: flexibility to create equal length of list
list([1])*3
t = L(1, match=(1,2,3)); t.items
t = L(1,2,5, match=(1,100,3)); t.items
t = L(5, match=(1,100,3)); t.items

###############################################################################
###############################################################################
# list.__len__ so it can do len(list)
len(list([1,2,4]))
# but L can do it yet, without `L.__len__`
t = L(1,2,3)
test_fail(lambda: len(t))
###############################################################################
@patch
def __len__(cls:L):
    """
    purpose:
    1. how can we give L the flexibility to do `len(L)` just like `len(list)`
    2. in fact, when we say length of L, we mean `len(self.items)` here
    """
    return len(cls.items)
################################################################################
# we have to write L.__len__ in order to do `len(t)`
t = L(1,2,3)
len(t)
t.__len__()


###############################################################################
###############################################################################
# list.__delitem__ so it can do the following
t = list([1,2,3])
t.__delitem__(0);t
t=L(1,2,3)
test_fail(lambda: t.__delitem__(0))
###############################################################################
@patch
def __delitem__(cls:L, i):
    """
    purpose:
    1. we want to flexibility to delete any item from L
    2. this is to remove any item from `self.items`
    3. `self.default` changes along with `self.items`
    """
    del(cls.items[i])
###############################################################################
# now, L.__delitem__ is created and added to L
t=L(1,2,3)
t.__delitem__(0); t.items
t.default


###############################################################################
###############################################################################
# list has list.__getitem__, so it can do the following
t = list([1,2,3])
hasattr(t, '__getitem__')
t[1]
t.__getitem__(1)
t[0:2]
# L has no attribute L.__getitem__, so it can't do it
t = L(1,2,3)
hasattr(t, '__getitem__')
test_fail(lambda: t[1])
#################################
# __getitem__ is also essential for many methods below, such as __repr__
test_fail(lambda: itertools.islice(map(str,t), 10), contains='not iterable')
test_fail(lambda: map(str,t), contains='not iterable')
###############################################################################
@patch
def __getitem__(cls:L, idx):
    """
    purpose:
    1. We want to do `t[idx]` as what list did above
    2. but we want more flexibility and power on indices
        b. index = list of int/indices with or without `[]` or `()`
        c. index = mask (list of T/F) without or with `[]` or `()`
    3. also, we want to flexibility to control return type:
        a. if idx is scalar, then return the individual item
        b. if idx is multiple, then return a new L instance
    """
    res = [cls.items[i] for i in _mask2idxs(idx)] if is_iter(idx) else cls.items[idx]

    if isinstance(res,(tuple,list)) and not isinstance(res,L): res = L(res)
    return res
###############################################################################
t = L(range(10)); t.items
t[0]
t[8]
t[(1,2,3)]
t[[1,2,3]]
t[-1,9,-4]
t[True, False, True, True, True, False, True, True]
t[[True, False, True, True, True, True]]
t[(True, False, True, True, True)]
# with L.__getitem__, L is iterable object
g = map(str,t)
next(g)

###############################################################################
###############################################################################
# because list has list.__repr__, so it can do the following reprensetation
t = list([1,2,3]); t
t[2]
# L has default L.__repr__ to only show the object name like the following
t = L(1,2,3); t
t.__repr__()
# to display L's content, we have to overwrite L.__repr__

###############################################################################
@patch
def __repr__(cls:L):
    """
    purpose:
    1. we want a nice way to present the collection of data L
    2. we want to see number of items inside, and the first 10 items
    3. but why `coll_repr(class)` can directly work on `L` instance?
        a. inside, `coll_repr` requires `L` to be iterable,
        b. because it uses `itertools.islice(map(str,t), 10)`
        c. `L.__getitem__` (not `L.__iter__`) makes L iterable
        d. it makes sense, because essential `L.__getitem__` turns
            `t[idx]` into `t.items[idx]`
        e. finally if idx is multiple, do `L(t.items[idx])` Otherwise,
            just `t.items[idx]`
    """
    return f'{coll_repr(cls)}'
###############################################################################
# now the new L.__repr__ can display L.items properly
t = L(range(100)); t
t.__repr__()
t[55]


###############################################################################
###############################################################################
t1 = [1,2,3]
t2 = [1,2,3]
hasattr(t1, '__eq__')
t1.__eq__(t2)
t1.__eq__([1,1,3])
t1 = L(1,2,3)
hasattr(t1, '__eq__')
t1.__eq__(t2)
##################################
@patch
def __eq__(cls:L,b):
    """
    purpose:
    1. L should at least have `L.__eq__` just like `list.__eq__` above
    2. but more flexible and power, should be able to compare list of any type
    3. so we combine `equals` and `all_equal` to compare list of all types
    4. `itertools.zip_longest(a,b` in `all_eqaul` requires iterables
    5. `L.__getitem__`ensures L to be iterable
    """
    return all_equal(b,cls)
###############################################################################
t1 = L(tensor(1,2,3))
t2 = L(tensor(1,2,3))
hasattr(t1, '__eq__')
t1.__eq__(t2)



###############################################################################
###############################################################################
t = [1,2,3]
hasattr(t, '__iter__')
g = t.__iter__()
next(g)
t = L([1,2,3]);t
hasattr(t, '__iter__')
###############################################################################
@patch
def __iter__(cls:L):
    """
    purpose:
    1. we want L to be turned into a generator with `L.__iter__`
        just like `list.__iter__`
    2. we would like to write it with pure python without builtin iter by C
    3. `(self[i] for i in range(len(self)))` is typical way of making generator
    """
    return (cls[i] for i in range(len(cls)))
###############################################################################
t = L([1,2,3])
hasattr(t, '__iter__')
g = t.__iter__()
next(g)

###############################################################################
###############################################################################
t = [1,2,3]
hasattr(t, '__mul__')
t.__mul__(3)
t*3
t = L(1,2,3)
hasattr(t, '__mul__')
###############################################################################
@patch
def __mul__ (a:L,b):
    """
    purpose:
    1. list.__mul__(3) is to triple the list into a new list
    2. L.__mul__(3) should be able to do the same, but return a L instance
    """
    return L(a.items*b)
###############################################################################
t = L(1,2,3)
hasattr(t, '__mul__')
# show_doc(t.__mul__)
t.__mul__(3)
t*3
###############################################################################
###############################################################################
t = [1,2,4]
hasattr(t, "__add__")
t.__add__([5])
t = L(1,2,3)
hasattr(t, "__add__")
###############################################################################
@patch
def __add__ (a:L,b):
    """
    purpose:
    1. list can add list into a longer list
    2. we want it for L, and much more flexible
    3. we want L can be added with not just list but anything else
    """
    return L(a.items+_listify(b))
###############################################################################
t=L(1,2,3)
hasattr(t, "__add__")
t.__add__([9])
t.__add__(9)
t.__add__(tensor(9))
t.__add__([tensor(9)])
t.__add__(range(9))
t + 10

###############################################################################
###############################################################################
t = [1,2,4]
hasattr(t, "__radd__")
t = L(1,2,3)
hasattr(t, "__radd__")
###############################################################################
@patch
def __radd__(a:L,b):
    """
    purpose:
    1. we want to add b to the front of L instance a, not normally at the end
    2. this is a feature that list does not have
    """
    return L(b)+a
###############################################################################
t = L(1,2,3)
hasattr(t, "__radd__")
t.__radd__(4)
5 + t
t

###############################################################################
###############################################################################
t = [1,2,4]
hasattr(t, "__addi__")
t = L(1,2,3)
hasattr(t, "__addi__")
###############################################################################
@patch
def __addi__(a:L,b):
    a.items += list(b)
    return a
###############################################################################
t = L(1,2,3)
hasattr(t, "__addi__")
t.__addi__([4])
t
t += [10]
t


###############################################################################
###############################################################################
t = [1,2,4]
hasattr(t, "__setitem__")
t[2] = 3; t
test_fail(lambda: t.__setitem__([0,1],9))
t = L(1,2,3)
hasattr(t, "__setitem__")
###############################################################################
@patch
def __setitem__(cls:L, idx, o):
    """
    "Set `idx` (can be list of indices, or mask, or int) items to `o` (which is broadcast if not iterable)"
    purpose:
    1. of course, we need to do `t[idx] = value`, but we want a lot more
    2. we want to setitem with multiple values

    steps:
    1. idx has to be either L or a list
    2. make sure 'o' is iterable rather than a scalar
    3. also `zip` requires both `idx` and `o` to be iterable
    4. assign each `o_` to `cls.items` using `list.__setitem__`
    """
    idx = idx if isinstance(idx,L) else _listify(idx)
    if not is_iter(o): o = [o]*len(idx)
    for i,o_ in zip(idx,o): cls.items[i] = o_
###############################################################################
t = L(1,2,3)
t.__setitem__([1,2], 9)
t
t = L(1,2,3)
t.__setitem__((1,0), (9,'9'))
t.items
t # same? not at all, they all turned into string by coll_repr


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
