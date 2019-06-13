from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
##############

from local.core import L, chk

@chk
def compose(*funcs: Callable, order=None):
    """
    purpose:
    1. sometimes, we got a number functions to run in series, and
    2. these funcs are even taking same args
    3. so, we will refactor the code and make life easier with `compose`
        3.1 all functions are organized into a L
        3.2 all functions are sorted by `order` using `L.sorted`
    4. then we create a `_inner()`:
        4.1 we loop through every function
        4.2 run the function with *args, **kwargs
        Note: *args, **kwargs are given by user from outside, see examples below
    """
    funcs = L(funcs)
    if order is not None: funcs = funcs.sorted(order)
    def _inner(x, *args, **kwargs):
        for f in L(funcs): x = f(x, *args, **kwargs)
        return x
    return _inner

f1 = lambda o,p=0: (o*2)+p
f2 = lambda o,p=1: (o+1)/p
f2(f1(3))
compose(f1,f2)(3) # x = 3, *args and **kwargs are None here
f2(f1(3,p=3),p=3)
compose(f1,f2)(3,p=3) # x = 3, p = 3 (args: p)
f1.order = 1 # f2 has no order attribute, but L.sorted will make it 0
compose(f1,f2, order="order")(3)
f1(f2(3))
