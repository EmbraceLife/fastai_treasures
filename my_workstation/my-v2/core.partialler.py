from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
##############
# `partialler(f, *args, order=None, **kwargs)`
# = Like `functools.partial` but also copies over docstring"
# = also set `order` too
# = returns a args-specified function of `f`

def partialler(f, *args, order=None, **kwargs):
    "Like `functools.partial` but also copies over docstring"
    fnew = partial(f,*args,**kwargs)
    fnew.__doc__ = f.__doc__
    if order is not None: fnew.order=order
    elif hasattr(f,'order'): fnew.order=f.order
    return fnew

def examples():

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
