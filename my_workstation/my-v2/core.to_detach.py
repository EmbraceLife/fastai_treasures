from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
#################

from local.core import apply, tensor

###################

def to_detach(b, cpu=True):
    """
    purpose:
    1. often we need to detach data from graph, we use `tensor.detach`
    2. but we want to detach tensors at all levels in a complex data object
        2.1 so we use `apply(_inner, x)` to do it recursively
        2.2 `_inner` is to detach everything
    3. so we want _inner to `detach` anything:
        3.1 non-tensor: just return x
        3.2 tensor: run x.detach()
            a. if cpu == True, return x.cpu()
            b. if not, return x
    """
    def _inner(x, cpu=True):
        if not isinstance(x,Tensor): return x
        x = x.detach() # detach from graph, no gradient required
        return x.cpu() if cpu else x
    return apply(_inner, b, cpu=cpu)

b = tensor(1,2)
to_detach(b, cpu=True)
b = [torch.Tensor([1,2]), tensor(3,4), tensor(5,7)]
to_detach(b, cpu=True)
t = tensor(1,2,3)
show_doc(t.detach)
