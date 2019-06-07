from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
###############

from local.core import apply, defaults, tensor

###############
# doc_imporve: add () to torch.cuda.is_available
# but it may be intentionally want the default to be on gpu

defaults.device = torch.device('cuda',0) if torch.cuda.is_available() else torch.device('cpu')

###############
# to_device(b, device=defaults.device) =
# > Recursively put `b` on `device`, by default on gpu

def to_device(b, device=defaults.device):
    "Recursively put `b` on `device`."
    def _inner(o): return o.to(device, non_blocking=True) if isinstance(o,Tensor) else o
    return apply(_inner, b)

def examples():
    t1,(t2,t3) = to_device([3,[tensor(3),tensor(2)]])

    test_eq((t1,t2,t3),(3,3,2))
    test_eq(t2.type(), "torch.cuda.LongTensor") # on my mac it is cpu
    test_eq(t3.type(), "torch.cuda.LongTensor")

################
# `to_cpu(b)` = Recursively map lists of tensors in `b ` to the cpu

def to_cpu(b):
    "Recursively map lists of tensors in `b ` to the cpu."
    return to_device(b,'cpu')

def examples():
    t3 = to_cpu(t3)
    test_eq(t3.type(), "torch.LongTensor")
    test_eq(t3, 2)
