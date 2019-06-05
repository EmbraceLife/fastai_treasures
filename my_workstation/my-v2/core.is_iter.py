from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

Tensor.ndim = property(lambda x: x.dim())
# export
def is_iter(o):
    "Test whether `o` can be used in a `for` loop"
    #Rank 0 tensors in PyTorch are not really iterable
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)

# pdb
is_iter([1])
is_iter(torch.tensor(1))
is_iter(torch.tensor([1,2]))
is_iter(o for o in range(3))
is_iter(range(3))

# nb
assert is_iter([1])
assert is_iter(torch.tensor(1))
assert is_iter(torch.tensor([1,2]))
assert (o for o in range(3))
