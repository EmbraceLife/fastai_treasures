from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import L, GetAttr, ifnone

def mk_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    """
    "Dynamically add a class containing `fld_names` to the caller's module"

    purpose:
    1. use a func to create class
    2.
    """
    # fill the dict `flds` with keys as `fld_names` and values as 'None'
    for f in fld_names: flds[f] = None
    # if `funcs` are provided, feed each `f.__name__` and `f` to `flds` the dict
    for f in L(funcs): flds[f.__name__] = f
    # get super class ready,
    sup = ifnone(sup, ())
    # if super is not a tuple, make it one
    if not isinstance(sup, tuple): sup=(sup,)
    # to get the model where the class is defined
    stk = inspect.stack()[1]
    mod = ifnone(inspect.getmodule(stk[0]), sys.modules['__main__'])

    # _init is to add funcs to match with fld_names as methods using both *args and **kwargs
    def _init(self, *args, **kwargs):
        for i,v in enumerate(args): setattr(self, fld_names[i], v)
        for k,v in kwargs.items(): setattr(self,k,v)

    # to print out all non-hidden and non-method attributes
    def _repr(self):
        return '\n'.join(f'{o}: {getattr(self,o)}' for o in set(dir(self))
                         if not o.startswith('_') and not isinstance(getattr(self,o), types.MethodType))

    # get __repr__ and __init__ assigned
    flds['__repr__'] = _repr
    flds['__init__'] = _init
    # create this new type of class
    res = type(nm, sup, flds)
    # add docs to the class
    if doc is not None: res.__doc__ = doc
    # assign `res` to `mod.nm` to put this new class in the module
    setattr(mod, nm, res)

show_doc(mk_class)

############################################
# use positional argument 'a' to assign `_t.a = None`
mk_class('_t', 'a') # nm = '_t', (one of) fld_names = 'a', no `funcs` to fill
t = _t()
t.a

#########################################
# use named arg `a=1` to assign `_t.a = 1`
mk_class('_t', a=1, sup=GetAttr)# nm='_t', one of **flds is {a:1}
t = _t()
t.a
assert(isinstance(t,GetAttr))

###############################
# a slight more complex example
def foo(self): return 1
mk_class('_t', # nm is class name
        'a', # 'a' is fed to class as one of `fld_names`, attributes
        sup=GetAttr, # nm's super class is GetAttr
        doc='test doc', # nm's doc is this
        funcs=foo, # funcs to be fed as class methods
        default="bee", # from GetAttr's usage
        _xtra=['upper', 'lower']) # from GetAttr's usage


t = _t( 3, # assign 3 to be the value of _t's first attribute `_t.a`
        b=2) # assign 2 to be the value of `_t.b`
test_eq(t.a, 3)
test_eq(t.b, 2)
test_eq(t.foo(), 1)
test_eq(t.__doc__, 'test doc')
t._xtra
t.default
t.upper()
t.lower()
t # __repr__ is to print out all its attributes

###############################################################################
###############################################################################
def wrap_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    """
    purpose:
    0. although we have `@patch` to automatically add a newly created func
        - as a method of an existing class
    1. what if the class is not previous available neither?
    2. can we create a class and a method altogether at once?
    3. yes, if we make `mk_class` into a decorator before a function creation
    """
    def _inner(f):
        mk_class(nm, *fld_names, sup=sup, doc=doc, funcs=L(funcs)+f, **flds)
        return f
    return _inner

@wrap_class('_t', a=2) # this decorator using `mk_class` to create a class
def bar(self,x): # this create a new func which automatically becomes a method
    return x+1

t = _t()
t.a
t.bar(3)
t
