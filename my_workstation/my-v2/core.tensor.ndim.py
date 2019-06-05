from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import tensor
# #### `Tensor.ndim`

Tensor.ndim = property(lambda x: x.dim())

# We add an `ndim` property to `Tensor` with same semantics as
# [numpy ndim](https://docs.scipy.org/doc/numpy/reference/generated/
# numpy.ndarray.ndim.html), which allows tensors to be used in matplotlib
# and other places that assume this property exists.

test_eq(torch.tensor([1,2]).ndim,1)
test_eq(torch.tensor(1).ndim,0)
test_eq(torch.tensor([[1]]).ndim,2)
torch.tensor([1,2]).shape
torch.tensor([1,2]).ndim
torch.tensor([[1]]).shape
torch.tensor([[1]]).ndim
tensor([[1]]).shape
tensor([[1]]).ndim
