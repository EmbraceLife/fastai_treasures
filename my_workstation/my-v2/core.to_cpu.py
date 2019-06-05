from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import defaults, tensor, apply, to_device

# put a list of items onto cpu for computation
def to_cpu(b):
    "Recursively map lists of tensors in `b ` to the cpu."
    return to_device(b,'cpu')

t1,(t2,t3) = to_device([3,[tensor(3),tensor(2)]])
t3 = to_cpu(t3)
test_eq(t3.type(), "torch.LongTensor")
test_eq(t3, 2)

to_cpu([3,[tensor(3),tensor(2)]])
