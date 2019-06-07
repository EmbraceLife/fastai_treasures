from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

################
from local.core import is_listy, tensor

#################
# `apply(func, x, *args, **kwargs)` = recursively apply func to `x`
# > `func` = any func
# > `x` = anything of a scalar, a list/tuple, or a dict

def apply(func, x, *args, **kwargs):
    "Apply `func` recursively to `x`, passing on args"
    if is_listy(x): return [apply(func, o, *args, **kwargs) for o in x]
    if isinstance(x,dict):  return {k: apply(func, v, *args, **kwargs) for k,v in x.items()}
    return func(x, *args, **kwargs)

def examples():
    apply(is_listy, tensor(1,2))
    apply(is_listy, [tensor(1,2), tensor(2,3)])
    apply(is_listy, {'a':tensor(1,2), 'b':tensor(2,3)})
