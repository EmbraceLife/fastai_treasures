from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

################
from local.core import is_listy, tensor, L

def apply(func, x, *args, **kwargs):
    """
    purpose:
    1. although `map(f, x)` can apply f to every element of x on one level
    2. but `map` can't dive deep recursively when element itself is iterable
    3. we can do three things with this func
        a. exactly like `map(f, x)` with `args` and `kwargs`
        b. when `x` is list-like, do map recursively on x, level by level
        c. when `x` is dict-like, do map recursively on x, level by level
    """
    if is_listy(x): return [apply(func, o, *args, **kwargs) for o in x]
    if isinstance(x,dict):  return {k: apply(func, v, *args, **kwargs) for k,v in x.items()}
    return func(x, *args, **kwargs)

list(map(str, L([1,2,3])))
apply(str, [1,2,3])
apply(str, [1, [[2,[3]], [[[9]]]]])
apply(str, {'a':{'a1': {'aa1':1}}, 'b':3})
