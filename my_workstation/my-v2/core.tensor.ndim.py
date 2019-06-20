from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import tensor

show_doc(property)

# a quick way to add property to a class
Tensor.ndim = property(lambda x: x.dim())

# We add an `ndim` property to `Tensor` with same semantics as
# [numpy ndim](https://docs.scipy.org/doc/numpy/reference/generated/
# numpy.ndarray.ndim.html), which allows tensors to be used in matplotlib
# and other places that assume this property exists.

tensor(0).ndim
tensor(5).ndim
tensor(1,2,3).shape
tensor(1,2,3).ndim
tensor([[1,4,4],[2,5,5]]).shape
tensor([[1],[4]]).ndim
######### learn the Property usage
Tensor.scalar = property(lambda x: x.dim()==0)
Tensor.vector = property(lambda x: x.dim()==1)
Tensor.matrix = property(lambda x: x.dim()==2)
Tensor.image = property(lambda x: x.dim()==3)
Tensor.video = property(lambda x: x.dim()==4)
tensor(0).scalar
tensor(1,2,3).scalar
