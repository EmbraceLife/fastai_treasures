from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

Tensor.ndim = property(lambda x: x.dim())

show_doc(is_iter) # it must be put first

# export
def is_iter(o):
    """
    why need is_iter?
    - really want to be sure whether something is iterable or not
    - but being `Iterable` or `Generator` does not guarantee it
    - `is_iter` tell us anything is really iterable or not.

    how to use it?
    - put everything into it `is_iter(o)`

    how does is_iter work?
    - to be really iterable must satistfy two conditions
        - `o` must be `Iterable` or `Generator`, and
        - `o` has either no `ndim` or its `ndim` is greater than 0
    """
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)

# simple examples
is_iter((1,2,3))
isinstance(tensor(1), (Iterable,Generator))
is_iter(tensor(5))
is_iter(tensor([5]))
is_iter([5])
is_iter(o for o in range(3))
is_iter(range(3))
is_iter(tensor([[1,2],[2,3]]))# only loop with first dimension
is_iter(array([[1,2],[3,4],[4,5]]))
is_iter(array(9))
isinstance(array(9), (Iterable,Generator))
getattr(array(9), 'ndim', None)
array((9,10)).ndim
is_iter(array((1,2)))
