from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

import copy
# %%
#export
def patch_to(cls):
    """
    "Decorator: add `f` to `cls`"

    why patch_to
    1. add another method to an existing class
        needs going back to class source and add a method
    2. life would be much easier to write a method/func anywhere and
        it will automatically add itself to a class
    3. we want such a feature be ready for any class to add methods

    steps:
    2. wrap `f` with its own copy `nf`
    3. set up `nf.__qualname__` by f"{cls.__name__}.{f.__name__}"
    4. setattr(cls, f.__name__, nf)
    5. return the `f`

    """
    def _inner(f):
        nf = copy.copy(f)
        # `functools.update_wrapper` when passing patched function to `Pipeline`, so we do it manually
        for o in functools.WRAPPER_ASSIGNMENTS: setattr(nf, o, getattr(f,o))
        nf.__qualname__ = f"{cls.__name__}.{f.__name__}"
        setattr(cls, f.__name__, nf)
        return f
    return _inner

class _T2():
    def __init__(self, o): self.foo = getattr(o,'foo',0) + 1


@patch_to(_T2)
def func1(x, a:bool): return a+2

t = _T2(1)
t.func1(1)

#export
def patch(f):
    "Decorator: add `f` to the first parameter's class (based on f's type annotations)"
    # set pdb here to walk through all the source
    cls = next(iter(f.__annotations__.values()))
    return patch_to(cls)(f)

@patch
def func(x:_T2, a:bool):
    "test"
    return a+2

t = _T2(1)
t.func(1)
t.func.__qualname__
