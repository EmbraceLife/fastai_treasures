from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
#################

from local.core import apply, tensor

###################
# `to_detach(b, cpu=True)`
# = detach lists of tensors in `b `; put them on the CPU if `cpu=True`


def to_detach(b, cpu=True):
    "Recursively detach lists of tensors in `b `; put them on the CPU if `cpu=True`."
    def _inner(x, cpu=True):
        if not isinstance(x,Tensor): return x
        x = x.detach()
        return x.cpu() if cpu else x
    return apply(_inner, b, cpu=cpu)

b = tensor(1,2)
to_detach(b, cpu=True)
b = [torch.Tensor([1,2]), tensor(3,4), tensor(5,7)]
to_detach(b, cpu=True)
