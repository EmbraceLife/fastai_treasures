from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import tensor
Tensor.ndim = property(lambda x: x.dim())
# export
def is_iter(o):
    """
    purpose:
    1. whether `o` can do a `for` loop is not straightforward
    2. it has to be Iterable, Generator first
    3. though `tensor(1)` satisfy step2 but can do a for loop really
    4. same to `array(9)`
    5. other things seem all can do for loop, see examples below
    """
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)

isinstance(tensor(1), (Iterable,Generator))
is_iter(tensor(5))
is_iter(tensor([5]))
is_iter([5])
is_iter(o for o in range(3))
is_iter(range(3))
is_iter(tensor([[1,2],[2,3]]))# only loop with first dimension
is_iter(array([[1,2],[3,4],[4,5]]))
for i in array([[1,2],[3,4],[4,5]]): pass
is_iter(array(9))
isinstance(array(9), (Iterable,Generator))
getattr(array(9), 'ndim', 1)
array(9).ndim
# nb
assert is_iter([1])
assert is_iter(torch.tensor(1))
assert is_iter(torch.tensor([1,2]))
assert (o for o in range(3))
