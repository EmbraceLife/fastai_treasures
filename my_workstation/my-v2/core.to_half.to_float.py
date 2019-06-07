from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
#################

from local.core import apply, tensor

##############
# `to_half(b)` = Recursively map lists of float tensors in `b` to FP16
def to_half(b):
    "Recursively map lists of tensors in `b ` to FP16."
    return apply(lambda x: x.half() if x.dtype not in [torch.int64, torch.int32, torch.int16] else x, b)

# `to_float(b)` = Recursively map lists of float tensors in `b` to float32

def to_float(b):
    "Recursively map lists of int tensors in `b ` to float."
    return apply(lambda x: x.float() if x.dtype not in [torch.int64, torch.int32, torch.int16] else x, b)

def examples():
    b = [tensor(1,2), tensor(1.3394858, 3.59483)]
    to_half(b)
    b = [tensor(1,2), tensor(3.3,4.1)]
    to_float(b)
    doc(b[0].float)
