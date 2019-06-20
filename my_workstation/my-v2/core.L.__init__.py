from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *
from local.core import _listify

show_doc(L)

@patch
def L_doc(cls:L):
    """
    why need `L`?
    - although with `_listify`, we can make everything a list
    - but don't we always wish for more features to work on a list of things?
    - why don't we add more flexibilities and functionalities beyond 'list'

    What new features `NewChkMeta` offer us with `L`?
    - create a new L object from values `items`
    - if `items` is instance of `L`, return the instance

    What new features `GetAttr` offer to `L`?
    - inherit from `GetAttr`, `L` can borrow others' methods
    - it actually can borrow all methods from `list` with `_xtra`
    """

show_doc(L.L_doc)

@patch
def __init__(cls:L, items=None, *rest, use_list=False, match=None):
    """
    why need `L`?
    - although with `_listify`, we can make everything a list
    - but don't we always wish for more features to work on a list of things?
    - why don't we add more flexibilities and functionalities beyond 'list'

    What new features `NewChkMeta` offer us with `L`?
    - create a new L object from values `items`
    - if `items` is instance of `L`, return the instance

    What new features `GetAttr` offer to `L`?
    - inherit from `GetAttr`, `L` can borrow others' methods
    - it actually can borrow all methods from `list` with `_xtra`

    #####################
    why need __init__?
    - obviously, we need a way to create such a L thing

    how to use __init__?
    - `L(None)`
    - `L(1,2,3)`
    - `L((1,2,3))`
    - `L(array(1,2,3))`
    - `L(tensor(1,2,3))`
    - `L(range(5, 10))`
    - `L(4, match=[1,2,3])`
    - `L(tensor(1,2,3), use_list=True)`
    - `L(...)` does not return anything, only manages items

    how does __init__ work?
    - first, we deal with `items` as None, turn it `[]`
    - then, we make `items` a list by `_listify(items)`
    - we can make `items` a strange list by `list(items)`
        - toggled by `use_list = True`
        - a single array or tensor break down into pieces
    - then we add flexibility to do `L.__init__(1,2,3)`
        - using `cls.items += list(rest)`,
        - just like we did in `core.tensor`
    - we can duplicate `items` `len(match)` times
    """
    items = [] if items is None else items
    cls.items = cls.default = list(items) if use_list else _listify(items)
    cls.items += list(rest)
    if match is not None:
        if len(cls.items)==1: cls.items = cls.items*len(match)
        else: assert len(cls.items)==len(match), 'Match length mismatch'

show_doc(L.__init__)
L(None)
L(1,2,3)
L((1,2,3))
L(array([1,2,3]))
L(tensor(1,2,3))
L(range(5, 10))
L(4, match=[1,2,3])
L(tensor(1,2,3), use_list=True)
