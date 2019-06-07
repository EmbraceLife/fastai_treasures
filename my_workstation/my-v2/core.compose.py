from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
##############

from local.core import L, chk

###############
# made_uncool for easy debug

###############
# `compose(*funcs: Callable, order=None)`
# = wrap func around func by their positional order or specified order
# = arguments for `compose` and `funcs` can be properly passed onto
# = `L.sorted` handles with order
# = `compose()` itself run inside `@chk`, then `_inner()` will run after
# Note: how `order` are passed to `compose`
# Noet: and how `x`, `p` are passed onto `funcs`

def compose(*funcs: Callable, order=None):
    "Create a function that composes all functions in `funcs`, passing along remaining `*args` and `**kwargs` to all"
    funcs = L(funcs)
    if order is not None:
        funcs = funcs.sorted(order)
    def _inner(x, *args, **kwargs):
        for f in L(funcs):
            x = f(x, *args, **kwargs)
        return x
    return _inner

compose = chk(compose)

def examples():
    # pdb
    f1 = lambda o,p=0: (o*2)+p
    f2 = lambda o,p=1: (o+1)/p
    f2(f1(3))
    compose(f1,f2)(3)
    f2(f1(3,p=3),p=3)
    compose(f1,f2)(3,p=3)
    f1.order = 1
    compose(f1,f2, order="order")(3)
    f1(f2(3))


    # nb
    f1 = lambda o,p=0: (o*2)+p
    f2 = lambda o,p=1: (o+1)/p
    test_eq(f2(f1(3)), compose(f1,f2)(3))
    test_eq(f2(f1(3,p=3),p=3), compose(f1,f2)(3,p=3))
    test_eq(f2(f1(3,  3),  3), compose(f1,f2)(3,  3))

    f1.order = 1
    test_eq(f1(f2(3)), compose(f1,f2, order="order")(3))

################
# official compact

@chk
def compose(*funcs: Callable, order=None):
    "Create a function that composes all functions in `funcs`, passing along remaining `*args` and `**kwargs` to all"
    funcs = L(funcs)
    if order is not None: funcs = funcs.sorted(order)
    def _inner(x, *args, **kwargs):
        for f in L(funcs): x = f(x, *args, **kwargs)
        return x
    return _inner
