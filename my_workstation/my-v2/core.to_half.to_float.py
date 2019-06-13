from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
#################

from local.core import apply, tensor

##############
# `to_half(b)` = Recursively map lists of float tensors in `b` to FP16
def to_half(b):
    """
    purpose:
    1. we sometimes want to convert x to float16 dtype through all levels
    2. apply(lambda: , x) make sure recursively deep
    3. we only consider two kinds of x/cases for converting
        3.1 group int: torch.int64, ...32, ...16 => do nothing
        3.2 everything else: torch.int8, torch.float... => convert by `x.half()`
        3.3 `x.half()` is to convert to float16
    "Recursively map lists of tensors in `b ` to FP16/float16."
    """
    return apply(lambda x: x.half() if x.dtype not in [torch.int64, torch.int32, torch.int16] else x, b)

# `to_float(b)` = Recursively map lists of float tensors in `b` to float32

def to_float(b):
    """
    purpose:
    1. we sometimes want to convert x to float32 dtype through all levels
    2. apply(lambda: , x) make sure recursively deep
    3. we only consider two kinds of x/cases for converting
        3.1 group int: torch.int64, ...32, ...16 => do nothing
        3.2 everything else: torch.int8, torch.float... => convert by `x.float()`
        3.3 `x.float()` is to convert to float32
    """
    return apply(lambda x: x.float() if x.dtype not in [torch.int64, torch.int32, torch.int16] else x, b)

# torch.int8, 16, 32, 64

b = [tensor(1,2), tensor(1.3394858, 3.59483)]
apply(lambda x: x.dtype, b)
b = to_half(b)
apply(lambda x: x.dtype, b)
b = [tensor(1,2), tensor(3.3,4.1)]
apply(lambda x: x.dtype, b)
b = to_float(b)
apply(lambda x: x.dtype, b)
show_doc(torch.float)
