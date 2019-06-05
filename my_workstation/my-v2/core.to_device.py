from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import defaults, tensor, apply

defaults = SimpleNamespace()
defaults.device = torch.device('cuda',0) if torch.cuda.is_available() else torch.device('cpu')

def to_device(b, device=defaults.device):
    "Recursively put `b` on `device`."
    def _inner(o): return o.to(device, non_blocking=True) if isinstance(o,Tensor) else o
    return apply(_inner, b)

t1,(t2,t3) = to_device([3,[tensor(3),tensor(2)]])
test_eq((t1,t2,t3),(3,3,2))
test_eq(t2.type(), "torch.LongTensor")
test_eq(t3.type(), "torch.LongTensor")
# test_eq(t2.type(), "torch.cuda.LongTensor")
# test_eq(t3.type(), "torch.cuda.LongTensor")

def to_device(b, device=defaults.device):
    "Recursively put `b` on `device`."
    def _inner(o):
        if isinstance(o,Tensor):
            # Performs Tensor dtype and/or device conversion
            return o.to(device, non_blocking=True)
        else:
            return o
    return apply(_inner, b)

t = to_device([3, tensor(3)])
t[1].type()
