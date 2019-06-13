from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc


def partialler(f, *args, order=None, **kwargs):
    """
    purpose:
    1. we know `partial(f, *args, **kwargs)` already made our life easier
    2. however, we want refactor more actions into this `partialler(f, ...)`
        2.1 of course, first we do the standard `partial(f, *args, **kwargs)`
                assigned to `fnew`
        2.2 we add `f.__doc__` to be the `fnew` func
        2.3 we add order attribute onto the `fnew` func if applicable
            a. order info can come from input arg `order`
            b. or from `f.order`
    3. return the `fnew`, which does a lot more than standard `partial`

    arguments:
    1. `f`: the function to be refactored
    2. `*args`: all positional args of `f`
    3. `order`: to add attribute info on `f.order`
    4. `**kwargs` : all named arguments from `f`
    """
    fnew = partial(f,*args,**kwargs)
    fnew.__doc__ = f.__doc__
    if order is not None: fnew.order=order
    elif hasattr(f,'order'): fnew.order=f.order
    return fnew


def _f(x,a=1): # this is the `f` func
    "test func" # `f.__doc__`
    return x+a
_f.order=1 # `f.order` is available

f = partialler(_f, a=2) # partialler take the same args as `f`
test_eq(f.order, 1)
f = partialler(_f, a=2, order=3) # you don't write *args, **kwargs here!
test_eq(f.__doc__, "test func")
test_eq(f.order, 3)
test_eq(f(3), _f(3,2))
