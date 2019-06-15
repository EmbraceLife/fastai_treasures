# %%
#default_exp core
# %%
#export
from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
# %%
device_id = 7
torch.cuda.set_device(device_id)
# %% markdown
# # Core
#
# > Basic functions used in the fastai library
# %%
# export
defaults = SimpleNamespace()
# %% markdown
# ## Foundational functions
# %% markdown
# ### Decorators
# %%
#export
def newchk(cls):
    "Class decorator to avoid recreating object passed to constructor"
    old_new,old_init  = cls.__new__,cls.__init__

    def _inner_new(cls, x=None, *args, **kwargs):
        if x is not None and isinstance(x,cls):
            x._newchk = 1
            return x
        res = old_new(cls)
        res._newchk = 0
        return res

    def _inner_init(self, *args, **kwargs):
        if self._newchk: return
        old_init(self, *args, **kwargs)

    cls.__new__  = functools.update_wrapper(_inner_new,  cls.__init__)
    cls.__init__ = functools.update_wrapper(_inner_init, cls.__init__)
    return cls
# %%
@newchk
class _T():
    "Testing"
    def __init__(self, o=None): self.foo = getattr(o,'foo',0) + 1

class _T2():
    def __init__(self, o): self.foo = getattr(o,'foo',0) + 1

t = _T(1)
test_eq(t.foo,1)
t2 = _T(t)
test_eq(t2.foo,1)

t = _T2(1)
test_eq(t.foo,1)
t2 = _T2(t)
test_eq(t2.foo,2)

test_eq(_T.__doc__, "Testing")
test_eq(str(inspect.signature(_T)), '(o=None)')
# %%
import copy
# %%
#export
def patch(f):
    "Decorator: add `f` to the first parameter's class (based on f's type annotations)"
    cls = next(iter(f.__annotations__.values()))
    nf = copy.copy(f)
    functools.update_wrapper(nf,f)
    nf.__qualname__ = f"{cls.__name__}.{f.__name__}"
    setattr(cls, f.__name__, nf)
    return f
# %%
@patch
def func(x:_T2, a:bool):
    "test"
    return a+2

t = _T2(1)
test_eq(t.func(1), 3)
test_eq(t.func.__qualname__, '_T2.func')
# %% markdown
# ### Type checking
# %% markdown
# Runtime type checking is handy, so let's make it easy!
# %%
#export core
#NB: Please don't move this to a different line or module, since it's used in testing `get_source_link`
def chk(f): return typechecked(always=True)(f)
# %% markdown
# Decorator for a function to check that type-annotated arguments receive arguments of the right type.
# %%
@chk
def test_chk(a:int=1): pass
# %%
test_chk(1)
test_chk()
# %%
test_fail(lambda: test_chk('a'), contains='"a" must be int')
# %% markdown
# ### Context managers
# %%
@contextmanager
def working_directory(path):
    "Change working directory to `path` and return to previous on exit."
    prev_cwd = Path.cwd()
    os.chdir(path)
    try: yield
    finally: os.chdir(prev_cwd)
# %% markdown
# ### Monkey-patching
# %%
#export
@patch
def ls(self:Path):
    "Contents of path as a list"
    return list(self.iterdir())
# %% markdown
# We add an `ls()` method to `pathlib.Path` which is simply defined as `list(Path.iterdir())`, mainly for convenience in REPL environments such as notebooks.
# %%
path = Path()
t = path.ls()
assert len(t)>0
t[0]
# %%
#hide
pkl = pickle.dumps(path)
p2 =pickle.loads(pkl)
test_eq(path.ls()[0], p2.ls()[0])
# %%
#export
def tensor(x, *rest):
    "Like `torch.as_tensor`, but handle lists too, and can pass multiple vector elements directly."
    if len(rest): x = (x,)+rest
    # Pytorch bug in dataloader using num_workers>0
    if isinstance(x, (tuple,list)) and len(x)==0: return tensor(0)
    res = torch.tensor(x) if isinstance(x, (tuple,list)) else as_tensor(x)
    if res.dtype is torch.int32:
        warn('Tensor is int32: upgrading to int64; for better performance use int64 input')
        return res.long()
    return res
# %%
test_eq(tensor(array([1,2,3])), torch.tensor([1,2,3]))
test_eq(tensor(1,2,3), torch.tensor([1,2,3]))
# %% markdown
# #### `Tensor.ndim`
# %%
#export
Tensor.ndim = property(lambda x: x.dim())
# %% markdown
# We add an `ndim` property to `Tensor` with same semantics as [numpy ndim](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.ndim.html), which allows tensors to be used in matplotlib and other places that assume this property exists.
# %%
test_eq(torch.tensor([1,2]).ndim,1)
test_eq(torch.tensor(1).ndim,0)
test_eq(torch.tensor([[1]]).ndim,2)
# %% markdown
# ### Documentation functions
# %%
#export core
def add_docs(cls, cls_doc=None, **docs):
    "Copy values from `docs` to `cls` docstrings, and confirm all public methods are documented"
    if cls_doc is not None: cls.__doc__ = cls_doc
    for k,v in docs.items():
        f = getattr(cls,k)
        if hasattr(f,'__func__'): f = f.__func__ # required for class methods
        f.__doc__ = v
    # List of public callables without docstring
    nodoc = [c for n,c in vars(cls).items() if isinstance(c,Callable)
             and not n.startswith('_') and c.__doc__ is None]
    assert not nodoc, f"Missing docs: {nodoc}"
    assert cls.__doc__ is not None, f"Missing class docs: {cls}"
# %%
#export core
def docs(cls):
    "Decorator version of `add_docs"
    add_docs(cls, **cls._docs)
    return cls
# %%
class _T:
    def f(self): pass
    @classmethod
    def g(cls): pass
add_docs(_T, "a", f="f", g="g")

test_eq(_T.__doc__, "a")
test_eq(_T.f.__doc__, "f")
test_eq(_T.g.__doc__, "g")
# %%
#export
def custom_dir(c, add:List):
    "Implement custom `__dir__`, adding `add` to `cls`"
    return dir(type(c)) + list(c.__dict__.keys()) + add
# %%
# export
def is_iter(o):
    "Test whether `o` can be used in a `for` loop"
    #Rank 0 tensors in PyTorch are not really iterable
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)
# %%
assert is_iter([1])
assert not is_iter(torch.tensor(1))
assert is_iter(torch.tensor([1,2]))
assert (o for o in range(3))
# %%
# export
def coll_repr(c, max=1000):
    "String repr of up to `max` items of (possibly lazy) collection `c`"
    return f'(#{len(c)}) [' + ','.join(itertools.islice(map(str,c), 10)) + ('...'
            if len(c)>10 else '') + ']'
# %%
test_eq(coll_repr(range(1000)), '(#1000) [0,1,2,3,4,5,6,7,8,9...]')
# %% markdown
# ## GetAttr -
# %%
#export
class GetAttr:
    "Inherit from this to have all attr accesses in `self._xtra` passed down to `self.default`"
    _xtra=[]
    def __getattr__(self,k):
        assert self._xtra, "Inherited from `GetAttr` but no `_xtra` attrs listed"
        if k in self._xtra: return getattr(self.default, k)
        raise AttributeError(k)
    def __dir__(self): return custom_dir(self, self._xtra)
# %%
class _C(GetAttr): default,_xtra = 'Hi',['lower']

t = _C()
test_eq(t.lower(), 'hi')
test_fail(lambda: t.upper())
assert 'lower' in dir(t)
# %% markdown
# ## L -
# %%
# export
def _mask2idxs(mask):
    mask = list(mask)
    if len(mask)==0: return []
    if isinstance(mask[0],bool): return [i for i,m in enumerate(mask) if m]
    return [int(i) for i in mask]

def _listify(o):
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, (str,np.ndarray,Tensor)): return [o]
    if is_iter(o): return list(o)
    return [o]
# %%
#export
@newchk
class L(GetAttr):
    "Behaves like a list of `items` but can also index with list of indices or masks"
    _xtra =  [o for o in dir(list) if not o.startswith('_')]

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
    def __invert__(self): return L(not i for i in self)
    def __mul__ (a,b): return L(a.items*b)
    def __add__ (a,b): return L(a.items+_listify(b))
    def __radd__(a,b): return L(b)+a
    def __addi__(a,b):
        a.items += list(b)
        return a

    def __getitem__(self, idx):
        "Retrieve `idx` (can be list of indices, or mask, or int) items"
        res = [self.items[i] for i in _mask2idxs(idx)] if is_iter(idx) else self.items[idx]
        if isinstance(res,(tuple,list)) and not isinstance(res,L): res = L(res)
        return res

    def __setitem__(self, idx, o):
        "Set `idx` (can be list of indices, or mask, or int) items to `o` (which is broadcast if not iterable)"
        idx = idx if isinstance(idx,L) else _listify(idx)
        if not is_iter(o): o = [o]*len(idx)
        for i,o_ in zip(idx,o): self.items[i] = o_

    def sorted(self, key=None, reverse=False):
        "New `L` sorted by `key`. If key is str then use `attrgetter`. If key is int then use `itemgetter`."
        if isinstance(key,str):   k=lambda o:getattr(o,key,0)
        elif isinstance(key,int): k=itemgetter(key)
        else: k=key
        return L(sorted(self.items, key=k, reverse=reverse))

    def mapped(self, f, *args, **kwargs): return L(map(partial(f,*args,**kwargs), self))
    def zipped(self):       return L(zip(*self))
    def itemgot(self, idx): return self.mapped(itemgetter(idx))
    def attrgot(self, k):   return self.mapped(lambda o:getattr(o,k,0))
    def tensored(self):     return self.mapped(tensor)
    def stack(self, dim=0): return torch.stack(list(self.tensored()), dim=dim)
    def cat  (self, dim=0): return torch.cat  (list(self.tensored()), dim=dim)
# %%
add_docs(L,
         mapped="Create new `L` with `f` applied to all `items`, passing `args` and `kwargs` to `f`",
         zipped="Create new `L` with `zip(*items)`",
         itemgot="Create new `L` with item `idx` of all `items`",
         attrgot="Create new `L` with attr `k` of all `items`",
         tensored="`mapped(tensor)`",
         stack="Same as `torch.stack`",
         cat="Same as `torch.cat`")
# %% markdown
# You can create an `L` from an existing iterable (e.g. a list, range, etc) and access or modify it with an int list/tuple index, mask, int, or slice. All `list` methods can also be used with `L`.
# %%
t = L(range(12))
test_eq(t, list(range(12)))
test_ne(t, list(range(11)))
t.reverse()
test_eq(t[0], 11)
t[3] = "h"
test_eq(t[3], "h")
t[3,5] = ("j","k")
test_eq(t[3,5], ["j","k"])
test_eq(t, L(t))
t
# %% markdown
# You can also modify an `L` with `append`, `+`, and `*`.
# %%
t = L()
test_eq(t, [])
t.append(1)
test_eq(t, [1])
t += [3,2]
test_eq(t, [1,3,2])
t = t + [4]
test_eq(t, [1,3,2,4])
t = 5 + t
test_eq(t, [5,1,3,2,4])
test_eq(L(1,2,3), [1,2,3])
test_eq(L(1,2,3), L(1,2,3))
t = L(1)*5
t = t.mapped(operator.neg)
test_eq(t,[-1]*5)
test_eq(~L([True,False,False]), L([False,True,True]))
# %%
def _f(x,a=0): return x+a
t = L(1)*5
test_eq(t.mapped(_f), t)
test_eq(t.mapped(_f,1), [2]*5)
test_eq(t.mapped(_f,a=2), [3]*5)
# %% markdown
# An `L` can be constructed from anything iterable, although tensors and arrays will not be iterated over on construction, unless you pass `use_list` to the constructor.
# %%
test_eq(L([1,2,3]),[1,2,3])
test_eq(L(L([1,2,3])),[1,2,3])
test_ne(L([1,2,3]),[1,2,])
test_eq(L('abc'),['abc'])
test_eq(L(range(0,3)),[0,1,2])
test_eq(L(o for o in range(0,3)),[0,1,2])
test_eq(L(tensor(0)),[tensor(0)])
test_eq(L([tensor(0),tensor(1)]),[tensor(0),tensor(1)])
test_eq(L(tensor([0.,1.1]))[0],tensor([0.,1.1]))
test_eq(L(tensor([0.,1.1]), use_list=True), [0.,1.1])  # `use_list=True` to unwrap arrays/tensors
# %% markdown
# If `match` is not `None` then the created list is same len as `match`, either by:
#
# - If `len(items)==1` then `items` is replicated,
# - Otherwise an error is raised if `match` and `items` are not already the same size.
# %%
test_eq(L(1,match=[1,2,3]),[1,1,1])
test_eq(L([1,2],match=[2,3]),[1,2])
test_fail(lambda: L([1,2],match=[1,2,3]))
# %% markdown
# ### Methods
# %%
show_doc(L.__getitem__)
# %%
t = L(range(12))
test_eq(t[1,2], [1,2])                # implicit tuple
test_eq(t[[1,2]], [1,2])              # list
test_eq(t[:3], [0,1,2])               # slice
test_eq(t[[False]*11 + [True]], [11]) # mask
test_eq(t[tensor(3)], 3)
# %%
show_doc(L.__setitem__)
# %%
t[4,6] = 0
test_eq(t[4,6], [0,0])
t[4,6] = [1,2]
test_eq(t[4,6], [1,2])
# %%
show_doc(L.mapped)
# %%
test_eq(L(range(4)).mapped(operator.neg), [0,-1,-2,-3])
# %%
show_doc(L.zipped)
# %%
t = L([[1,2,3],'abc'])
test_eq(t.zipped(), [(1, 'a'),(2, 'b'),(3, 'c')])
# %%
show_doc(L.itemgot)
# %%
test_eq(t.itemgot(1), [2,'b'])
# %%
show_doc(L.attrgot)
# %%
a = [SimpleNamespace(a=3,b=4),SimpleNamespace(a=1,b=2)]
test_eq(L(a).attrgot('b'), [4,2])
# %%
show_doc(L.sorted)
# %%
test_eq(L(a).sorted('a').attrgot('b'), [2,4])
# %% markdown
# ### Tensor methods
# %% markdown
# There are shortcuts for `torch.stack` and `torch.cat` if your `L` contains tensors or something convertible. You can manually convert with `tensored`.
# %%
t = L(([1,2],[3,4]))
# %%
test_eq(t.tensored(), [tensor(1,2),tensor(3,4)])
test_eq(t.stack(), tensor([[1,2],[3,4]]))
test_eq(t.cat(), tensor([1,2,3,4]))
# %% markdown
# ## Utility functions
# %% markdown
# ### Basics
# %%
# export
def ifnone(a, b):
    "`b` if `a` is None else `a`"
    return b if a is None else a
# %% markdown
# Since `b if a is None else a` is such a common pattern, we wrap it in a function. However, be careful, because python will evaluate *both* `a` and `b` when calling `ifnone` (which it doesn't do if using the `if` version directly).
# %%
test_eq(ifnone(None,1), 1)
test_eq(ifnone(2   ,1), 2)
# %%
#export
def get_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    "Dynamically create a class containing `fld_names`"
    for f in fld_names: flds[f] = None
    for f in L(funcs): flds[f.__name__] = f
    sup = ifnone(sup, ())
    if not isinstance(sup, tuple): sup=(sup,)

    def _init(self, *args, **kwargs):
        for i,v in enumerate(args): setattr(self, fld_names[i], v)
        for k,v in kwargs.items(): setattr(self,k,v)

    def _repr(self):
        return '\n'.join(f'{o}: {getattr(self,o)}' for o in set(dir(self))
                         if not o.startswith('_') and not isinstance(getattr(self,o), types.MethodType))

    if not sup: flds['__repr__'] = _repr
    flds['__init__'] = _init
    res = type(nm, sup, flds)
    if doc is not None: res.__doc__ = doc
    return res
# %%
_t = get_class('_t', 'a')
t = _t()
test_eq(t.a, None)
# %% markdown
# Most often you'll want to call `mk_class`, since it adds the class to your module. See `mk_class` for more details and examples of use (which also apply to `get_class`).
# %%
#export
def mk_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    "Create a class using `get_class` and add to the caller's module"
    stk = inspect.stack()[1]
    mod = ifnone(inspect.getmodule(stk[0]), sys.modules['__main__'])
    res = get_class(nm, *fld_names, sup=sup, doc=doc, funcs=funcs, **flds)
    setattr(mod, nm, res)
# %% markdown
# Any `kwargs` will be added as class attributes, and `sup` is an optional (tuple of) base classes.
# %%
mk_class('_t', a=1, sup=GetAttr)
t = _t()
test_eq(t.a, 1)
assert(isinstance(t,GetAttr))
# %% markdown
# A `__init__` is provided that sets attrs for any `kwargs`, and for any `args` (matching by position to fields), along with a `__repr__` which prints all attrs. The docstring is set to `doc`. You can pass `funcs` which will be added as attrs with the function names.
# %%
def foo(self): return 1
mk_class('_t', 'a', sup=GetAttr, doc='test doc', funcs=foo)

t = _t(3, b=2)
test_eq(t.a, 3)
test_eq(t.b, 2)
test_eq(t.foo(), 1)
test_eq(t.__doc__, 'test doc')
t
# %%
#export
def wrap_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    "Decorator: makes function a method of a new class `nm` passing parameters to `mk_class`"
    def _inner(f):
        mk_class(nm, *fld_names, sup=sup, doc=doc, funcs=L(funcs)+f, **flds)
        return f
    return _inner
# %%
@wrap_class('_t', a=2)
def bar(self,x): return x+1

t = _t()
test_eq(t.a, 2)
test_eq(t.bar(3), 4)
t
# %%
# export
def noop (x=None, *args, **kwargs):
    "Do nothing"
    return x
# %%
noop()
test_eq(noop(1),1)
# %%
# export
def noops(self, x, *args, **kwargs):
    "Do nothing (method)"
    return x
# %%
mk_class('_t', foo=noops)
test_eq(_t().foo(1),1)
# %% markdown
# ### Collection functions
# %%
#export
def tuplify(o, use_list=False, match=None):
    "Make `o` a tuple"
    return tuple(L(o, use_list=use_list, match=match))
# %%
test_eq(tuplify(None),())
test_eq(tuplify([1,2,3]),(1,2,3))
test_eq(tuplify(1,match=[1,2,3]),(1,1,1))
# %%
#export
def replicate(item,match):
    "Create tuple of `item` copied `len(match)` times"
    return (item,)*len(match)
# %%
t = [1,1]
test_eq(replicate([1,2], t),([1,2],[1,2]))
test_eq(replicate(1, t),(1,1))
# %%
#export
def uniqueify(x, sort=False, bidir=False, start=None):
    "Return the unique elements in `x`, optionally `sort`-ed, optionally return the reverse correspondance."
    res = list(OrderedDict.fromkeys(x).keys())
    if start is not None: res = L(start)+res
    if sort: res.sort()
    if bidir: return res, {v:k for k,v in enumerate(res)}
    return res
# %%
# test
test_eq(set(uniqueify([1,1,0,5,0,3])),{0,1,3,5})
test_eq(uniqueify([1,1,0,5,0,3], sort=True),[0,1,3,5])
v,o = uniqueify([1,1,0,5,0,3], bidir=True)
test_eq(v,[1,0,5,3])
test_eq(o,{1:0, 0: 1, 5: 2, 3: 3})
v,o = uniqueify([1,1,0,5,0,3], sort=True, bidir=True)
test_eq(v,[0,1,3,5])
test_eq(o,{0:0, 1: 1, 3: 2, 5: 3})
# %%
# export
def setify(o): return o if isinstance(o,set) else set(L(o))
# %%
# test
test_eq(setify(None),set())
test_eq(setify('abc'),{'abc'})
test_eq(setify([1,2,2]),{1,2})
test_eq(setify(range(0,3)),{0,1,2})
test_eq(setify({1,2}),{1,2})
# %%
#export
def is_listy(x):
    "`isinstance(x, (tuple,list,L))`"
    return isinstance(x, (tuple,list,L,slice))
# %%
assert is_listy([1])
assert is_listy(L([1]))
assert is_listy(slice(2))
assert not is_listy(torch.tensor([1]))
# %%
#export
def range_of(x):
    "All indices of collection `x` (i.e. `list(range(len(x)))`)"
    return list(range(len(x)))
# %%
test_eq(range_of([1,1,1,1]), [0,1,2,3])
# %%
# export
def mask2idxs(mask):
    "Convert bool mask or index list to index `L`"
    return L(_mask2idxs(mask))
# %%
test_eq(mask2idxs([False,True,False,True]), [1,3])
test_eq(mask2idxs(torch.tensor([1,2,3])), [1,2,3])
# %% markdown
# ### File and network functions
# %%
def bunzip(fn):
    "bunzip `fn`, raising exception if output already exists"
    fn = Path(fn)
    assert fn.exists(), f"{fn} doesn't exist"
    out_fn = fn.with_suffix('')
    assert not out_fn.exists(), f"{out_fn} already exists"
    with bz2.BZ2File(fn, 'rb') as src, out_fn.open('wb') as dst:
        for d in iter(lambda: src.read(1024*1024), b''): dst.write(d)
# %%
f = Path('files/test.txt')
if f.exists(): f.unlink()
bunzip('files/test.txt.bz2')
t = f.open().readlines()
test_eq(len(t),1)
test_eq(t[0], 'test\n')
f.unlink()
# %% markdown
# ### Tensor functions
# %%
#export
def apply(func, x, *args, **kwargs):
    "Apply `func` recursively to `x`, passing on args"
    if is_listy(x): return [apply(func, o, *args, **kwargs) for o in x]
    if isinstance(x,dict):  return {k: apply(func, v, *args, **kwargs) for k,v in x.items()}
    return func(x, *args, **kwargs)
# %%
#export
def to_detach(b, cpu=True):
    "Recursively detach lists of tensors in `b `; put them on the CPU if `cpu=True`."
    def _inner(x, cpu=True):
        if not isinstance(x,Tensor): return x
        x = x.detach()
        return x.cpu() if cpu else x
    return apply(_inner, b, cpu=cpu)
# %%
#export
def to_half(b):
    "Recursively map lists of tensors in `b ` to FP16."
    return apply(lambda x: x.half() if x.dtype not in [torch.int64, torch.int32, torch.int16] else x, b)
# %%
#export
def to_float(b):
    "Recursively map lists of int tensors in `b ` to float."
    return apply(lambda x: x.float() if x.dtype not in [torch.int64, torch.int32, torch.int16] else x, b)
# %%
#export
defaults.device = torch.cuda.current_device() if torch.cuda.is_available else torch.device('cpu')
# %%
#export
def to_device(b, device=defaults.device):
    "Recursively put `b` on `device`."
    def _inner(o): return o.to(device, non_blocking=True) if isinstance(o,Tensor) else o
    return apply(_inner, b)
# %%
t1,(t2,t3) = to_device([3,[tensor(3),tensor(2)]])
test_eq((t1,t2,t3),(3,3,2))
test_eq(t2.type(), "torch.cuda.LongTensor")
test_eq(t3.type(), "torch.cuda.LongTensor")
# %%
#export
def to_cpu(b):
    "Recursively map lists of tensors in `b ` to the cpu."
    return to_device(b,'cpu')
# %%
t3 = to_cpu(t3)
test_eq(t3.type(), "torch.LongTensor")
test_eq(t3, 2)
# %%
def to_np(x):
    "Convert a tensor to a numpy array."
    return x.data.cpu().numpy()
# %%
t3 = to_np(t3)
test_eq(type(t3), np.ndarray)
test_eq(t3, 2)
# %%
#export
def item_find(x, idx=0):
    "Recursively takes the `idx`-th element of `x`"
    if is_listy(x): return item_find(x[idx])
    if isinstance(x,dict):
        key = list(x.keys())[idx] if isinstance(idx, int) else idx
        return item_find(x[key])
    return x
# %%
#export
def find_device(b):
    "Recursively search the device of `b`."
    return item_find(b).device
# %%
test_eq(find_device(t2), defaults.device)
test_eq(find_device([t2,t2]), defaults.device)
test_eq(find_device({'a':t2,'b':t2}), defaults.device)
test_eq(find_device({'a':[[t2],[t2]],'b':t2}), defaults.device)
# %%
#export
def find_bs(b):
    "Recursively search the batch size of `b`."
    return item_find(b).shape[0]
# %%
x = torch.randn(4,5)
test_eq(find_bs(x), 4)
test_eq(find_bs([x, x]), 4)
test_eq(find_bs({'a':x,'b':x}), 4)
test_eq(find_bs({'a':[[x],[x]],'b':x}), 4)
# %%
def np_func(f):
    "Convert a function taking and returning numpy arrays to one taking and returning tensors"
    def _inner(*args, **kwargs):
        nargs = [to_np(arg) if isinstance(arg,Tensor) else arg for arg in args]
        return tensor(f(*nargs, **kwargs))
    functools.update_wrapper(_inner, f)
    return _inner
# %% markdown
# This decorator is particularly useful for using numpy functions as fastai metrics, for instance:
# %%
from sklearn.metrics import f1_score

@np_func
def f1(inp,targ): return f1_score(targ, inp)

a1,a2 = array([0,1,1]),array([1,0,1])
t = f1(tensor(a1),tensor(a2))
test_eq(f1_score(a1,a2), t)
assert isinstance(t,Tensor)
# %% markdown
# ### Functions on functions
# %%
# export
@chk
def compose(*funcs: Callable, order=None):
    "Create a function that composes all functions in `funcs`, passing along remaining `*args` and `**kwargs` to all"
    funcs = L(funcs)
    if order is not None: funcs = funcs.sorted(order)
    def _inner(x, *args, **kwargs):
        for f in L(funcs): x = f(x, *args, **kwargs)
        return x
    return _inner
# %%
f1 = lambda o,p=0: (o*2)+p
f2 = lambda o,p=1: (o+1)/p
test_eq(f2(f1(3)), compose(f1,f2)(3))
test_eq(f2(f1(3,p=3),p=3), compose(f1,f2)(3,p=3))
test_eq(f2(f1(3,  3),  3), compose(f1,f2)(3,  3))
# %%
f1.order = 1
test_eq(f1(f2(3)), compose(f1,f2, order="order")(3))
# %%
#export
def mapper(f):
    "Create a function that maps `f` over an input collection"
    return lambda o: [f(o_) for o_ in o]
# %%
func = mapper(lambda o:o*2)
test_eq(func(range(3)),[0,2,4])
# %%
#export
def partialler(f, *args, order=None, **kwargs):
    "Like `functools.partial` but also copies over docstring"
    fnew = partial(f,*args,**kwargs)
    fnew.__doc__ = f.__doc__
    if order is not None: fnew.order=order
    elif hasattr(f,'order'): fnew.order=f.order
    return fnew
# %%
def _f(x,a=1):
    "test func"
    return x+a
_f.order=1

f = partialler(_f, a=2)
test_eq(f.order, 1)
f = partialler(_f, a=2, order=3)
test_eq(f.__doc__, "test func")
test_eq(f.order, 3)
test_eq(f(3), _f(3,2))
# %% markdown
# ### Sorting objects from before/after
# %% markdown
# Transforms and callbacks will have run_after/run_before attributes, this function will sort them to respect those requirements (if it's possible). Also, sometimes we want a tranform/callback to be run at the end, but still be able to use run_after/run_before behaviors. For those, the function checks for a toward_end attribute (that needs to be True).
# %%
#export
def _is_instance(f, gs):
    tst = [g if type(g) in [type, 'function'] else g.__class__ for g in gs]
    for g in tst:
        if isinstance(f, g) or f==g: return True
    return False

def _is_first(f, gs):
    for o in L(getattr(f, 'run_after', None)):
        if _is_instance(o, gs): return False
    for g in gs:
        if _is_instance(f, L(getattr(g, 'run_before', None))): return False
    return True

def sort_by_run(fs):
    end = L(getattr(f, 'toward_end', False) for f in fs)
    inp,res = L(fs)[~end] + L(fs)[end], []
    while len(inp) > 0:
        for i,o in enumerate(inp):
            if _is_first(o, inp):
                res.append(inp.pop(i))
                break
        else: raise Exception("Impossible to sort")
    return res
# %%
class Tst(): pass
class Tst1():
    run_before=[Tst]
class Tst2():
    run_before=Tst
    run_after=Tst1

tsts = [Tst(), Tst1(), Tst2()]
test_eq(sort_by_run(tsts), [tsts[1], tsts[2], tsts[0]])

Tst2.run_before,Tst2.run_after = Tst1,Tst
test_fail(lambda: sort_by_run([Tst(), Tst1(), Tst2()]))

def tst1(x): return x
tst1.run_before = Tst
test_eq(sort_by_run([tsts[0], tst1]), [tst1, tsts[0]])

class Tst1():
    toward_end=True
class Tst2():
    toward_end=True
    run_before=Tst1
tsts = [Tst(), Tst1(), Tst2()]
test_eq(sort_by_run(tsts), [tsts[0], tsts[2], tsts[1]])
# %% markdown
# ### Other helpers
# %%
#export
def num_cpus():
    "Get number of cpus"
    try:                   return len(os.sched_getaffinity(0))
    except AttributeError: return os.cpu_count()

defaults.cpus = num_cpus()
# %%
#export
def add_props(f, n=2):
    "Create properties passing each of `range(n)` to f"
    return (property(partial(f,i)) for i in range(n))
# %%
class _T(): a,b = add_props(lambda i,x:i*2)

t = _T()
test_eq(t.a,0)
test_eq(t.b,2)
# %% markdown
# This is a quick way to generate, for instance, *train* and *valid* versions of a property. See `DataBunch` definition for an example of this.
# %%
#export
def make_cross_image(bw=True):
    "Create a tensor containing a cross image, either `bw` (True) or color"
    if bw:
        im = torch.zeros(5,5)
        im[2,:] = 1.
        im[:,2] = 1.
    else:
        im = torch.zeros(3,5,5)
        im[0,2,:] = 1.
        im[1,:,2] = 1.
    return im
# %%
plt.imshow(make_cross_image(), cmap="Greys");
# %%
plt.imshow(make_cross_image(False).permute(1,2,0));
# %% markdown
# ## Export -
# %%
#hide
from local.notebook.export import notebook2script
notebook2script(all_fs=True)
# %%
