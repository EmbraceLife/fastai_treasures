#AUTOGENERATED! DO NOT EDIT! File to edit: dev/02_data_pipeline.ipynb (unless otherwise specified).

__all__ = ['get_func', 'show_title', 'Func', 'Sig', 'SelfFunc', 'Self', 'positional_annotations', 'noop_tfm',
           'PrePostInitMultiMeta', 'Transform', 'transform', 'compose_tfms', 'Pipeline', 'get_samples', 'TfmdList',
           'TfmdDS', 'setattr_parent']

from ..imports import *
from ..test import *
from ..core import *
from ..notebook.showdoc import show_doc

def get_func(t, name, *args, **kwargs):
    """
    "Get the `t.name` (potentially partial-ized with `args` and `kwargs`) or `noop` if not defined"

    why get_func(...)
    1. sometimes getting the plain method, t.name is not enough, 
    1. we want t.name with specified args, kwargs
    2. why not allow get_func(...) to do both

    Note: 
    1. it just get methods, not do calculation
    """
    f = getattr(t, name, noop)
    return f if not (args or kwargs) else partial(f, *args, **kwargs)

def show_title(o, ax=None, ctx=None):
    """
    "Set title of `ax` to `o`, or print `o` if `ax` is `None`"

    why show_title(...)
    1. if we really got an image, we can set `o` as the image's title
    1. if no image, then just print out `o`
    2. `ax` and `ctx` seem used interchangeably
    """
    ax = ifnone(ax,ctx)
    if ax is None: print(o)
    else: ax.set_title(o)

class Func():
    """
    "Basic wrapper around a `name` with `args` and `kwargs` 
    to call on a given type"

    why Func():
    1. we can get a method easily like `math.pow`
    2. but what if we want the method to be `math.pow(x, 2)`
    3. what if we want to get a list [math.pow(x,2), torch.pow(x, 2)]
    4. how cool if we can get it by Func('pow', a=2)([math, torch])

    why __init__(self, name, *args, **kwargs)
    1. we get method name and its args, kwargs ready

    why __repr__(self)
    1. we just want to see method name and its args, kwargs

    why _get(self, t)
    1. we want to use get_func(...) to get method flexibly with args and kwargs

    why __call__(self, t)
    1. we want Func('pow', args, kwargs)(t) to get us:
        a. either t.pow with args, and kwargs
        b. or t1.pow(x, args, kwargs), t2.pow(x, args, kwargs)...
    """
    def __init__(self, name, *args, **kwargs): 
        """
        why __init__(...)
        1. we get method name and its args, kwargs ready
        """
        self.name,self.args,self.kwargs = name,args,kwargs
    def __repr__(self): 
        """
        why __repr__(self)
        1. we just want to see method name and its args, kwargs
        """
        return f'sig: {self.name}({self.args}, {self.kwargs})'
    def _get(self, t): 
        """
        why _get(self, t)
        1. we want to use get_func(...) to get method flexibly with args and kwargs
        """
        return get_func(t, self.name, *self.args, **self.kwargs)
    def __call__(self,t): 
        """
        why __call__(self, t)
        1. we want Func('pow', args, kwargs)(t) to get us:
            a. either t.pow with args, and kwargs
            b. or t1.pow(x, args, kwargs), t2.pow(x, args, kwargs)...
        
        Note: 
        1. returns methods with args, kwargs, not calculations by the methods
        """
        return L(t).mapped(self._get) if is_listy(t) else self._get(t)

class _Sig():
    """
    Sig = _Sig()
    `Sig` is just sugar-syntax to create a `Func` object more easily with the syntax `Sig.name(*args, **kwargs)`.

    why _Sig():
    1. because we want the use of Func(...) much easier
    1. how about use it in the following way:
        a. Sig.sqrt()(math)(4)
        b. Sig.pow()(math)(4,2)
        c. use , to allow vscode to display signiture

    Note:
    1. differ from SelfFunc, Sig considers args and kwargs in the end

    Example
    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    Sig.sqrt()(math)(4)
    Sig.pow()(math)(4,2)
    Sig.pow()([math, torch]) # return two methods, can't do calc easily here
    """
    def __getattr__(self,k):
        def _inner(*args, **kwargs): return Func(k, *args, **kwargs)
        return _inner

Sig = _Sig()

class SelfFunc():
    """
    "Search for `name` attribute and call it with `args` and `kwargs` on any object it's passed."

    why SelfFunc()
    1. given Sig, SelfFunc is very identical, but maybe one step shorter
    2. more important, Sig and Func can't return method/s, not designed to deliver calculations primarily
    3. why don't we design SelfFunc to deliver calculations (even multiple) as returns

    Note:
    1. differ from Sig, SelfFunc considers args and kwargs from __init__

    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    SelfFunc('sqrt')(tensor(4.0))
    SelfFunc('pow', 2)(tensor(4.0))
    SelfFunc('pow', 2)([tensor(4), tensor(5.0)])
    """
    def __init__(self, nm, *args, **kwargs): 
        "get method name and args, kwargs ready"
        self.nm,self.args,self.kwargs = nm,args,kwargs
    def __repr__(self): 
        "print out method names, args, kwargs"
        return f'self: {self.nm}({self.args}, {self.kwargs})'
    def __call__(self, o):
        "use o.method calculate as o has data inside, args, and kwargs are given by __init__ "
        if not is_listy(o): 
            return getattr(o,self.nm)(*self.args, **self.kwargs)
        else: 
            return [getattr(o_,self.nm)(*self.args, **self.kwargs) for o_ in o]

class _SelfFunc():
    """
    why SelfFunc() and Self?
    1. because we are crazy about typing the least codes
    2. previously we have, still too long?
        - SelfFunc('pow', 2)([tensor(4), tensor(5.0)])
    3. why not 
        - Self.pow(3)([tensor(4), tensor(7.0)])

    Examples:
    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    Self.sqrt()(tensor(4.0))
    Self.pow(3)([tensor(4.0), tensor(7.0)])
    """
    def __getattr__(self,k):
        def _inner(*args, **kwargs): return SelfFunc(k, *args, **kwargs)
        return _inner

Self = _SelfFunc()


def positional_annotations(f):
    """
    "Get list of annotated types for all positional params, or None if no annotation"

    Why positional_annotations(f):
    1. just want to know all the positional arguments types (not keyword argument)

    Note: 
    1. the source code has two if on the same line, very confusing
    2. my guess is the second if run first and then the first if else 
    3. check it out when having time!!

    Examples:
    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    def f1(x, y:float): return x+y
    def f2(a, b=2): return a
    def f3(a:int, b:float=2): return a
    positional_annotations(f1)# [None, float]
    positional_annotations(f2)# [None]
    positional_annotations(f3)# [int]
    """
    sig = inspect.signature(f)
    return [p.annotation if p.annotation != inspect._empty else None
            for p in sig.parameters.values() if p.default == inspect._empty and p.kind != inspect._VAR_KEYWORD]

from multimethod import multimeta,DispatchError

def _get_ret(func):
    """
    "Get the return annotation or type of `func`"

    Example:
    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    from local.data.pipeline import _get_ret
    def f1(x) -> float: return x
    _get_ret(f1) # float
    def f2(x) -> Tuple[float,float]: return x
    _get_ret(f2) # [float,float]
    """
    ann = getattr(func,'__annotations__', None)
    if not ann: return None
    typ = ann.get('return')
    return list(typ.__args__) if getattr(typ, '_name', '')=='Tuple' else typ

def noop_tfm(x,*args,**kwargs): 
    """
    why noop_tfm(x,*args,**kwargs)?
    1. sometimes, we need to a tfm which does nothing
    2. but to be useful, it can return data and all the positional args 

    Examples:
    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    noop_tfm(1) # 1
    noop_tfm(1,2,3) # (1,2,3)
    """
    return (x,*args) if len(args) > 0 else x

class PrePostInitMultiMeta(multimeta):
    """
    "Like `PrePostInit` but inherits `multimeta`"

    why PrePostInitMultiMeta(multimeta)?
    1. the source code is exactly the same as PrePostInitMeta
    2. only difference is super class is not type but multimedia
    3. so, we want the same functionalities but for multimedia
    4. we want to Transform to inherit from multimedia than type
    """
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        def _pass(self, *args,**kwargs): pass
        for o in ('__init__', '__pre_init__', '__post_init__'):
            if not hasattr(x,o): setattr(x,o,_pass)
        old_init = x.__init__

        @functools.wraps(old_init)
        def _init(self,*args,**kwargs):
            self.__pre_init__()
            old_init(self, *args,**kwargs)
            self.__post_init__()
        setattr(x, '__init__', _init)
        return x

class Transform(metaclass=PrePostInitMultiMeta):
    """
    "A function that `encodes` if `filt` matches, and optionally `decodes`, with an optional `setup`"

    Why Transform(metaclass=PrePostInitMultiMeta)?
    1. Transform is crucial in data augmentation, deserve a class
    2. we want a few class attributes to make sure every tfm has all those attributes and the default values

    What are the class attributes and default values
    1. `order`: 0
    2. add_before_setup: False 
    3. filt, t, state_args : None

    Examples
    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    tfm = Transform()
    tfm.order, tfm.add_before_setup, tfm.t, tfm.filt, tfm.state_args
    """
    order,add_before_setup,filt,t,state_args = 0,False,None,None,None

    def __init__(self,encodes=None,decodes=None):
        """
        why __init__(self,encodes=None,decodes=None)?
        1. you want an object of Transform, you need __init__
        2. the essence of a tfm is basically encodes and decodes 
        3. we need a way to get encodes ready
            a. either from args `encodes` to create a brand new
            b. or from an existing tfm object (self) who is running this __init__ here
            c. if the existing tfm has no encodes, do noop_tfm 
        4. the way to get decodes is the same
        5. set self.t = None (default is None too)

        Note: 
        1. both Transform.__init__ and __post_init__ get run 
        2. through multimethod.__call__
            a. self[tuple(map(type, args))](*args, **kwargs)
        3. is this to ensure type get checked???

        Examples
        from local.imports import *
        from local.core import *
        from local.data.pipeline import *
        tfm = Transform()
        tfm.encodes, tfm.decodes, tfm.t
        tfm.encodes(3), tfm.decodes(4)
        """
        self.encodes = getattr(self, 'encodes', noop_tfm) if encodes is None else encodes
        self.decodes = getattr(self, 'decodes', noop_tfm) if decodes is None else decodes
        self.t = None

    def __post_init__(self):
        """
        why __post_init__(self)?
        1. further make sure noop_tfm loaded if no encodes nor decodes

        Example: use of __post_init__
        class _DummyTfm(Transform):
            def __init__(self): pass #Pass init so that decodes isn't defined
            def encodes(self, x): return x+1
        dt = _DummyTfm()
        t = dt(4)
        dt.decode(t) # Decodes was still set at post init as noop_tfm
        """
        self.encodes = getattr(self, 'encodes', noop_tfm)
        self.decodes = getattr(self, 'decodes', noop_tfm)

    def _apply(self, fs, x, filt):
        """
        why _apply(self, fs, x, filt)?
        1. because we want to see what each single func (encodes or decodes) do to a data sample
        2. we want extra flexibility and power
        3. we want to see a single func with multiple args can do to a data sample
            - fs is a single func but can take multiple args, so x has to be list-like (arg1, arg2, ...), see example 1
            - self.t is to descript fs args
        4. we want to see multiple funcs with single args can do to data samples
            - fs is a group of funcs but with single arg, and x has to be multiple (arg_f1, arg_f2), see example 2
        4. How about multiple funcs in fs, and multiple args for either func, 
            - it is not working yet or not considered???
            - problem: due to `positional_annotations(gs)`
        5. ??? 
            if is_listy(self.t) and len(positional_annotations(gs)) != len(self.t):
                gs = [self._get_func(fs,t_) for t_ in self.t]
                if len(gs) == 1: gs = gs[0]
        5. special case 2: self.filt can force _apply do nothing
            a. `filt` is some dataset index (e.g. provided by `DataSource`)
            a. if self.filt is strange, do nothing and return x
            a. strange => if self.filt is not None and not match with input filt
        Examples
        from local.imports import *
        from local.core import *
        from local.data.pipeline import *
        from multimethod import multimeta,DispatchError
        example 1 ============>
        def dummy_tfm(x:float,y:float): return [x+y,y] # x**y
        tfm = Transform(dummy_tfm)
        t = positional_annotations(dummy_tfm) # types of positional args 
        tfm.accept_types(t)
        tfm((2,3)) # __call__, _apply(..t,filt)
        example 2 ============>
        def dummy_tfm(x:float): return x**2
        tfm = Transform([dummy_tfm, operator.neg])
        tfm((2,3)) # __call__, _apply(..t,filt)
        """
        if self.filt is not None and self.filt!=filt: return x
        if self.t:
            gs = self._get_func(fs, self.t)
            if is_listy(self.t) and len(positional_annotations(gs)) != len(self.t):
                gs = [self._get_func(fs,t_) for t_ in self.t]
                if len(gs) == 1: gs = gs[0]
        else: gs=fs
        if is_listy(gs): 
            return tuple(f(x_) for f,x_ in zip(gs,x))
        return gs(*L(x)) if is_listy(self.t) else gs(x)

    def _get_func(self,f,t,ret_partial=True):
        """
        why _get_func(self,f,t,ret_partial=True)?
        1. basically, we want to extract the method/func from object `f`
        1. but we want it to be more flexible and powerful to handle different cases
        2. what if => `f` to have no __func__ => so just use `f` (usually, a normal func has no __func__)
        3. what if => `self.t` or `t` (type) can't idx the __func__ from `f`, => use noop_tfm
        4. so we intend to get specific __func__ from `f` using `self.t` as idx 
            c. add more flexibity => toggle ret_partial to use partial(f, self)
            d. just return f

        Note:
        cases 3, 4 not yet met

        Examples: see _apply
        """
        if not hasattr(f,'__func__'): return f
        idx = (object,) + tuple(t) if is_listy(t) else (object,t)
        try: f = f.__func__[idx]
        except DispatchError: return noop_tfm
        return partial(f,self) if ret_partial else f

    def accept_types(self, t): 
        """
        # We can't create encodes/decodes here since patching might change things later
        # So we call _get_func in _apply instead

        it seems to suggest `t` is type of encodes and decodes
        so, this is to set the type

        Examples:
        class _Add(Transform):
            def encodes(self, x, y): return (x+y,y)
            def decodes(self, x, y): return (x-y,y)
        addt = _Add()
        addt.t
        addt.accept_types([float,float])
        t = addt((1,2))
        addt.decode(t) # (1,2))
        #tfm.accept_types([int,float]) Fails for now and needs a class with encodes
        """
        self.t = t

    def return_type(self):
        """
        Why return_type(self)?
        1. because we want to be sure the return type of encodes
        2. to be sure about func of encodes, we need _get_func
        3. then use _get_ret to find out return type 

        Note: 
        - not used in other methods of Transform

        Examples 
        from local.imports import *
        from local.core import *
        from local.data.pipeline import *
        from multimethod import multimeta,DispatchError

        #Check type is properly changed at dispatch
        class _AddOne(Transform):
            def encodes(self, x:int)->str: return x+1 # priority 3
            def encodes(self, x:float):       return x*2 # floatArg
            def encodes(self, x:int)->float:  return x**2 # priority 2
            def encodes(self, x:int)->int: return x+10 # priority 1
            def encodes(self, x:int, y:float)->int: return x+y # twoArgs
            def decodes(self, x:int):   return x-1
            def decodes(self, x:float): return x/2

        tfm = _AddOne()
        tfm.accept_types(float)
        tfm.return_type()# float
        tfm.accept_types(int)
        tfm.return_type() 
        tfm.accept_types([int,float])# run encodes twoArgs
        tfm.return_type() 
        tfm((5, 5.0))
        tfm.accept_types([float, int]) # run floatArg and run priority 1
        tfm.return_type() 
        tfm((5, 5.0)) # run encode priority 1, and floatArg
        """
        g = self._get_func(self.encodes, self.t, False)
        if is_listy(self.t) and len(positional_annotations(g))-1 != len(self.t):
            return [_get_ret(self._get_func(self.encodes,t_,False)) or t_ for t_ in self.t]
        return _get_ret(g) or self.t

    def __call__(self, x, filt=None): 
        """
        why __call__(self, x, filt=None)
        1. when we call a tfm object, we want to apply encodes onto data x

        Examples: see effect on filt
        class _FiltAddOne(Transform):
            filt=1
            def encodes(self, x): return x+1
            def decodes(self, x): return x-1
        addt = _FiltAddOne()
        addt(4,filt=1)# 5, just normal apply since filt == self.filt
        addt(4,filt=0)# 4, special case, filt != self.filt, just return x 

        Examples:
        # we can have multiple encodes (one func each), self.t (type) help to choose each encodes to use
        class _AddOne(Transform):
            def encodes(self, x:numbers.Integral): return x+1
            def encodes(self, x:float): return x*2
            def decodes(self, x:numbers.Integral): return x-1
        addt = _AddOne()
        addt.encodes
        addt.accept_types(float)
        start = 1
        t = addt(start)
        addt.decode(t) # if no match just use noop_tfm
        # we can use multiple values in self.t to make multiple use of encodes and decodes 
        addt.accept_types([float, int, float])
        start = (1,2,3)
        t = addt(start)
        addt.decode(t) # (2,2,6))
        """
        return self._apply(self.encodes, x, filt)
    def decode  (self, x, filt=None): 
        """
        why decode  (self, x, filt=None): 
        1. when we do tfm.decode(), we actually apply decodes to data x

        Examples:
        from local.imports import *
        from local.core import *
        from local.data.pipeline import *
        from multimethod import multimeta,DispatchError

        #Using supertype encodes/decodes, we have a hacky way, might want to simplify it.
        class _AddOne(Transform):
            def encodes(self, x:numbers.Integral): return x+1
            def encodes(self, x:int): return self._get_func(self.encodes, numbers.Integral)(x)*2
            def decodes(self, x:numbers.Integral): return x-1
            def decodes(self, x:int): return self._get_func(self.decodes, numbers.Integral)(x/2)
            
        tfm = _AddOne()
        start = 2
        tfm.accept_types(numbers.Integral)
        tfm.return_type()
        t = tfm(start)
        tfm.decode(t)
        tfm.accept_types(int)
        tfm.return_type()
        t = tfm(start)
        tfm.decode(t) # why this returns a float
        """
        return self._apply(self.decodes, x, filt)
    def __getitem__(self, x): 
        """
        why __getitem__(self, x)
        1. any loop work require this method to work
        2. however, a little strange here
            a. x is a data rather than idx
            b. because we return self(x) here => apply encodes onto data x

        Examples:
        from local.imports import *
        from local.core import *
        from local.data.pipeline import *
        tfm = Transform(operator.neg, decodes=operator.neg)
        t = tfm(4) # __call__
        tfm[4] # __getitem__
        tfm.decode(t) # decode()
        """
        return self(x) # So it can be used as a `Dataset`

def transform(cls):
    """
    "Decorator for registering a new `encodes` or `decodes` function in a tranform `cls`"

    why transform(cls)?
    1. why not have a very easy way to add additional encodes and decodes?

    How to use it?
    Examples 
    from local.imports import *
    from local.core import *
    from local.data.pipeline import *
    from multimethod import multimeta,DispatchError
    class _AddOne(Transform):
        def encodes(self, x:numbers.Integral): return x+1
        def encodes(self, x:float): return x*2
        def decodes(self, x:numbers.Integral): return x-1
    @transform(_AddOne)
    def decodes(self, x:float): return x/2

    addt.accept_types([float, int, float])
    t = addt((1,2,3))
    addt.decode(t)
    """
    def _inner(f):
        if   f.__name__=='encodes': cls.encodes.register(f)
        elif f.__name__=='decodes': cls.decodes.register(f)
        else: raise Exception('Function must be "encodes" or "decodes"')
    return _inner

def compose_tfms(x, tfms, func_nm='__call__', reverse=False, **kwargs):
    """
    "Apply all `func_nm` attribute of `tfms` on `x`, maybe in `reverse` order"

    Why compose_tfms(x, tfms, func_nm='__call__', reverse=False, **kwargs)
    1. after knowing what each tfm can do on x, we need them to work together on x
    2. so we want to order tfms in a line for execution upon x
    3. with __call__, we can order encodes of tfms in a line to transform x upon each other
    4. with 'decode', we can order decodes of tfms in a line to reverse x back to original state

    Examples:
    class _AddOne(Transform):
        def encodes(self, x): return x+1
        def decodes(self, x): return x-1
    tfms = [_AddOne(), Transform(torch.sqrt)]
    t = compose_tfms(tensor([3.]), tfms)
    compose_tfms(t, tfms, 'decodes') # tensor([1.]))
    compose_tfms(tensor([4.]), tfms, reverse=True) # tensor([3.]))
    """
    if reverse: tfms = reversed(tfms)
    for tfm in tfms: x = getattr(tfm,func_nm,noop)(x, **kwargs)
    return x

class Pipeline():
    """
    "A pipeline of composed (for encode/decode) transforms, setup with types"

    Why Pipeline()?
    1. given compose_tfms can order and stack tfms together and apply onto x, 
    2. what else can Pipeline(funcs, t) do for us?
        - although compose_tfms stack tfms funcs with order for execution
        - we want the power and flexibility to do the same and more for Tranform objects
    3. compose_tfms help us to encode and decode across a line of tfms, 
        - but we want to show the origin data in appropriate state
        - self.t, self.t_show are introduced to solve this problem
    """
    def __init__(self, funcs=None, t=None):
        """
        What does __init__ do?
        - basically to construct a Pipeline object
            - provide funcs for transformation
            - provide `t` for tfms selection?

        How exactly we build a Pipeline object?
        - if we gives no inputs to `Pipeline()`, 
            - then the object has the following attributes
            - `self.fs` as [], and `self.t_show`, `self.final_t` as None
        - if we give Pipeline() a few funcs (Transform objects or just funcs), we enumerate through the funcs:
            - we will sort funcs by pushing into `self.fs` by their `order` value
            - make sure all funcs are Transform objects
            - trace each func's inputs types t, and t_show method, along the execution order line
            - finally trace the `self.final_t` type
        - Question: if type is for display or show, why not in the reserve order?
            - maybe, show is done through decode, which need to trace back
            - if __init__ can trace from start to end for type with show, then
            - decode can trace back to the first type with show from the end
        
        Note: 
        - Pipeline() can take in a pipeline instance to use its funcs

        Examples ====>
        from local.imports import *
        from local.core import *
        from local.data.pipeline import *
        from multimethod import multimeta,DispatchError
        # example 1
        pipe1 = Pipeline()
        # example 2
        class String():
            @staticmethod
            def show(o, ctx=None, **kwargs): return show_title(str(o), ctx=ctx)
        class floatTfm(Transform):
            def encodes(self, x): return float(x)
            def decodes(self, x): return int(x)
        float_tfm=floatTfm()
        def neg(x) -> String: return -x
        neg_tfm = Transform(neg, neg) 
        pipe2 = Pipeline([neg_tfm, float_tfm]) # stack two tfms inside
        """
        if isinstance(funcs, Pipeline): funcs = funcs.fs
        self.fs,self.t_show = [],None
        if len(L(funcs)) == 0: self.final_t = t
        else:
            for i,f in enumerate(L(funcs).sorted(key='order')):
                if not isinstance(f,Transform): f = Transform(f)
                f.accept_types(t)
                self.fs.append(f)
                t = f.return_type()
                if self.t_show is None and hasattr(t, 'show'): self.t_idx,self.t_show = i,t
            self.final_t = t

    def new(self, t=None): 
        """
        why new(self, t=None)?
        - when you already got a pipeline object, how to create a new Pipeline object with new info on `t`?
        """
        return Pipeline(self, t)

    def __repr__(self): 
        """
        why __repr__(self)
        - when we print out a pipeline object, we want to see its funcs
        - funcs can be Transform objects or even pipelines
        """
        return f"Pipeline over {self.fs}"

    def setup(self, items=None):
        """
        what does it do?
        - whether to add self.fs to tfms
        - whether to ask other classes' setup to apply to items
        
        # During the setup, the `Pipeline` starts with no transform and adds them one at a time, so that during its setup, each transfrom get the items processed up to its point and not after. 
        
        # Depending on the attribute `add_before_setup`, the transform is added after the setup (default behaivor) so it's not called on the items used for the setup, or before (in which case it's called on the values used for setup).
        """
        tfms,self.fs = self.fs,[]
        for t in tfms:
            if t.add_before_setup:     self.fs.append(t)
            if hasattr(t, 'setup'):    t.setup(items)
            if not t.add_before_setup: self.fs.append(t)

    def __call__(self, o, filt=None): 
        """
        What does __call__(self, o, filt=None) do?
        - basically we do compose_tfms with self.fs onto o
        - if self.fs is empty, just do noop_tfms

        Examples ==> continue from __init__ examples
        t1=pipe1(1)
        t2=pipe2(2)

        Example on filt =====>
        from local.imports import *
        from local.core import *
        from local.data.pipeline import *
        from multimethod import multimeta,DispatchError
        class _FiltAddOne(Transform):
            filt=1
            def encodes(self, x): return x+1
            def decodes(self, x): return x-1
        class String():
            @staticmethod
            def show(o, ctx=None, **kwargs): return show_title(str(o), ctx=ctx)
        class floatTfm(Transform):
            def encodes(self, x): return float(x)
            def decodes(self, x): return int(x)
        float_tfm=floatTfm()
        def neg(x) -> String: return -x
        neg_tfm = Transform(neg, neg) 
        #Check filtering is properly applied
        pipe = Pipeline([neg_tfm, float_tfm, _FiltAddOne()])
        start = 2
        pipe(start) # default filt = None, but _FillAddOne.filt = 1, so _FiltAddOne() is disenabled when _apply()
        pipe(start, filt=1) # not both filt is 1, _FiltAddOne() enabled
        pipe(start, filt=0) # disabled
        [pipe.decode(pipe(start, filt=t), filt=t) for t in [None, 0, 1]]
        """
        return compose_tfms(o, self.fs, filt=filt)
    def decode  (self, i, filt=None): 
        """
        Why decode  (self, i, filt=None)
        - simple to reverse encodes or call, for viewing the original state of data
        - it is to run __call__ with func_name `decode` and reverse the funcs order

        Examples: ===> continue from __init__ and __call__ examples
        pipe2.decode(t2)
        """
        return compose_tfms(i, self.fs, func_nm='decode', reverse=True, filt=filt)
    #def __getitem__(self, x): return self(x)
    #def decode_at(self, idx): return self.decode(self[idx])
    #def show_at(self, idx):   return self.show(self[idx])

    def show(self, o, ctx=None, filt=None, **kwargs):
        """
        why show(self, o, ctx=None, filt=None, **kwargs):
        - upon decode, we use show to present the original state in a more appropriate way

        how to do it?
        - if no show type available, then just do decode, that's it
        - otherwise, we only decode the encoded data back to the point where show type begin 
            - not all the way to the starting point
        - display the decoded data

        Examples: ===> built from above examples
        pipe2 = Pipeline([neg_tfm, float_tfm]) # stack two tfms inside
        t = pipe2(2)
        type(t)
        pipe2.decode(t)
        #show decodes up to the point of the first transform that introduced the type that shows, not included
        pipe2.show(t)
        # Check opposite order
        pipe3 = Pipeline([float_tfm,neg_tfm])
        t = pipe3(2)
        # `show` comes from String on the last transform so only this one is decoded
        pipe3.show(t)#  '2.0')
        """
        if self.t_show is None: return self.decode(o, filt=filt)
        o = compose_tfms(o, self.fs[self.t_idx:], func_nm='decode', reverse=True, filt=filt)
        return self.t_show.show(o, ctx=ctx, **kwargs)

add_docs(Pipeline,
         __call__="Compose `__call__` of all `tfms` on `o`",
         decode="Compose `decode` of all `tfms` on `i`",
         new="Create a new `Pipeline`with the same `tfms` and a new initial `t`",
         show="Show item `o`",
         setup="Go through the transforms in order and call their potential setup on `items`")

def get_samples(b, max_rows=10):
    if isinstance(b, Tensor): return b[:max_rows]
    return zip(*L(get_samples(b_, max_rows) if not isinstance(b,Tensor) else b_[:max_rows] for b_ in b))

@docs
class TfmdList(GetAttr):
    "A `Pipeline` of `tfms` applied to a collection of `items`"
    _xtra = 'decode __call__ show'.split()

    def __init__(self, items, tfms, do_setup=True, parent=None):
        self.items,self.parent = L(items),parent
        self.default = self.tfms = Pipeline(tfms)
        if do_setup: self.setup()

    def __getitem__(self, i, filt=None):
        "Transformed item(s) at `i`"
        its = self.items[i]
        if is_iter(i):
            if not is_iter(filt): filt = L(filt for _ in i)
            return L(self.tfms(it, filt=f) for it,f in zip(its,filt))
        return self.tfms(its, filt=filt)

    def setup(self): self.tfms.setup(self)
    def subset(self, idxs): return self.__class__(self.items[idxs], self.tfms, do_setup=False, parent=self)
    def decode_at(self, idx, filt=None):
        return self.decode(self.__getitem__(idx,filt=filt), filt=filt)
    def show_at(self, idx, filt=None, **kwargs):
        return self.show(self.__getitem__(idx,filt=filt), filt=filt, **kwargs)
    def __eq__(self, b): return all_equal(self, b)
    def __len__(self): return len(self.items)
    def __iter__(self): return (self[i] for i in range_of(self))
    def __repr__(self): return f"{self.__class__.__name__}: {self.items}\ntfms - {self.tfms}"

    _docs = dict(setup="Transform setup with self",
                 decode_at="Decoded item at `idx`",
                 show_at="Show item at `idx`",
                 subset="New `TfmdList` that only includes items at `idxs`")

def _maybe_flat(t): return t[0] if len(t) == 1 else tuple(t)

class TfmdDS(TfmdList):
    def __init__(self, items, tfms=None, tuple_tfms=None, do_setup=True):
        if tfms is None: tfms = [None]
        self.items = items
        self.tfmd_its = [TfmdList(items, t, do_setup=do_setup, parent=self) for t in tfms]
        self.__post_init__(items, tuple_tfms, do_setup)

    def __post_init__(self, items, tuple_tfms, do_setup):
        #To avoid dupe code with DataSource
        self.tfms = [it.tfms for it in self.tfmd_its]
        self.tuple_tfms = Pipeline(tuple_tfms, t=[it.tfms.final_t for it in self.tfmd_its])
        if do_setup: self.setup()

    def __getitem__(self, i, filt=None):
        its = _maybe_flat([it.__getitem__(i, filt=filt) for it in self.tfmd_its])
        if is_iter(i):
            if len(self.tfmd_its) > 1: its = zip(*L(its))
            if not is_iter(filt): filt = L(filt for _ in i)
            return L(self.tuple_tfms(it, filt=f) for it,f in zip(its,filt))
        return self.tuple_tfms(its, filt=filt)

    def decode(self, o, filt=None):
        o = self.tuple_tfms.decode(o, filt=filt)
        if not is_listy(o): o = [o]
        return _maybe_flat([it.decode(o_, filt=filt) for o_,it in zip(o,self.tfmd_its)])

    def decode_batch(self, b, filt=None): return [self.decode(b_, filt=filt) for b_ in get_samples(b)]

    def show(self, o, ctx=None, filt=None, **kwargs):
        if self.tuple_tfms.t_show is not None: return self.tuple_tfms.show(o, ctx=ctx, filt=filt, **kwargs)
        o = self.tuple_tfms.decode(o, filt=filt)
        if not is_listy(o): o = [o]
        for o_,it in zip(o,self.tfmd_its): ctx = it.show(o_, ctx=ctx, filt=filt, **kwargs)
        return ctx

    def setup(self): self.tuple_tfms.setup(self)

    def subset(self, idxs):
        return self.__class__(self.items[idxs], self.tfms, self.tuple_tfms, do_setup=False)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.items}\ntfms - {self.tfms}\ntuple tfms - {self.tuple_tfms}"

add_docs(TfmdDS,
         "A `Dataset` created from raw `items` by calling each element of `tfms` on them",
         __getitem__="Call all `tfms` on `items[i]` then all `tuple_tfms` on the result",
         decode="Compose `decode` of all `tuple_tfms` then all `tfms` on `i`",
         decode_batch="`decode` all sample in a the batch `b`",
         show="Show item `o` in `ctx`",
         setup="Go through the transforms in order and call their potential setup on `items`",
         subset="New `TfmdDS` that only includes items at `idxs`")

def setattr_parent(o, k, v):
    if getattr(o, 'parent', False): setattr_parent(o.parent, k, v)
    if getattr(o, 'dsrc', False): setattr_parent(o.dsrc, k, v)
    setattr(o, k, v)
