from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L

def add_docs(cls, cls_doc=None, **docs):
    """
    purpose:
    1. ever thinking of write cls docs and methods docs together in one places
    2. and automatically added onto the cls and all its public methods
    3. we can store class docstring into `cls_doc` and
    4. and store a dict like {'func1':'this is func1', 'func2': 'this is func2'} inside `docs`

    steps:
    1. we can directly add `cls_doc` onto `cls.__doc__`
    2. we open the dict `docs` into `k` and `v`,
        a. get each method with `getattr(cls, k)` and assigned to `f`
        b. if `hasattr(f, '__func__')`, reassign `f.__func__` to `f`
        c. then assign `v` to `f.__doc__` as its docstring
    3. check all variables inside the dict `vars(cls)`
        a. if a variable `c` is callable, not start with '_', and has no doc
        b. then append `n` (name of c) to the list `nodoc`
    4. make sure to send a warning message if `nodoc` is not empty
    5. make sure to send a warning message if `cls.__doc__` is None
    """
    if cls_doc is not None: cls.__doc__ = cls_doc
    for k,v in docs.items():
        f = getattr(cls,k)
        if hasattr(f,'__func__'): f = f.__func__ # required for class methods
        f.__doc__ = v
    nodoc = []
    for n,c in vars(cls).items():
        if isinstance(c,Callable) and not n.startswith('_') and c.__doc__ is None:
            nodoc.append(n)
    assert not nodoc, f"Missing docs: {nodoc}"
    assert cls.__doc__ is not None, f"Missing class docs: {cls.__name__}"

def docs(cls):
    """
    "Decorator version of `add_docs"

    purpose:
    1. add_docs(cls, cls_doc, **docs) is great to add docs
    2. but we have to prepare three things separately:
        a. get class ready
        b. create the string for `cls_doc`
        c. create a dict for all methods docs in `docs`
    3. we want to be lazy by
        a. just adding a dict of docstring for cls and methods
        b. it is done together with building the class
        c. just write a dict of strings, that's it!
    """
    add_docs(cls, **cls._docs)
    return cls

@docs
class C():
    def func1(): pass
    def func2(): pass
    _docs = {'cls_doc':'this is C',
             'func1':'this is func1',
             'func2':'this is func2'}

c = C()
c.__doc__
c.func1.__doc__
c.func2.__doc__

add_docs(L,
         mapped="Create new `L` with `f` applied to all `items`",
         zipped="Create new `L` with `zip(*items)`",
         itemgot="Create new `L` with item `idx` of all `items`",
         attrgot="Create new `L` with attr `k` of all `items`",
         tensored="`mapped(tensor)`",
         stack="Same as `torch.stack`",
         cat="Same as `torch.cat`")
