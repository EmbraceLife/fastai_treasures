
from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import *

#export
def get_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    """
    "Dynamically create a class containing `fld_names`"

    why get_class(...)
    - because we want to easily create a class with specific attributes
    - we want super class, attributes, methods easily added

    how to use get_class(...)
    - `nm`: the class name you want to create
    - `*fld_names`: multiple attribute names you want to add
    - `sup`: the super class you want to add
    - `doc`: the class doc you want to add
    - `funcs`: the methods you want to add to your class
    - `**flds`: a dict of attribute names and contents you want to add

    how to create get_class(...)
    - make `fld_names` to be keys of `flds` and None as their values
    - make `funcs` names as keys of `flds` and `funcs` as their values
    - make `sup` a tuple, even when `sup` is empty `()`
    - create an `_init` method of `get_class(...)`
        - to provide two ways of creating attributes with values
        - 1. `*args` are to provide values for `*fld_names`
        - 2. `**kwargs` are provided as attribute names and values
    - create `_repr` to print out the class
        - to print out the class attribute names and values
        - make sure the attributes are not hidden with '_'
        - make sure the attributes are not MethodType
    - if no super class available, make `_repr` the new class `__repr__`
    - make `_init` the new class `__init__`
    - put the new class onto your module
    - add the `doc` onto the new class if available
    - return the new class

    Note:
    - often you will use `mk_class` instead, as it adds class to your module
    """
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

    # def _repr(self):
    #     return '\n'.join(f'{o}: {getattr(self,o)}' for o in set(dir(self))
    #                      if not o.startswith('_')) #and not isinstance(getattr(self,o), types.MethodType))

    if not sup: flds['__repr__'] = _repr
    flds['__init__'] = _init
    res = type(nm, sup, flds)
    if doc is not None: res.__doc__ = doc
    return res

###########
_t = get_class('_t', 'a'); _t
t = _t();t
module(t)
module(_t)
module(mk_class)
