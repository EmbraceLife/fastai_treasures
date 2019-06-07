from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

##################
# `tensor(x, *rest)` = return a tensor from many different types below
# `x` = scalar, tuple, list, array
# `rest` = a few numbers like (1,2,3)

def tensor(x, *rest):
    "Like `torch.as_tensor`, but handle lists too, and can pass multiple vector elements directly."
    if len(rest): x = (x,)+rest
    # Pytorch bug in dataloader using num_workers>0
    if isinstance(x, (tuple,list)) and len(x)==0: return tensor(0)
    res = torch.tensor(x) if isinstance(x, (tuple,list)) else as_tensor(x)
    if res.dtype is torch.int32:
        warn('Tensor is int32: upgrading to int64; for better performance use int64 input')
        return res.long()
    return res

# to pdb
tensor(array([1,2,3]))
tensor(1,2,3)
x = array([1,2,3])
x = 0
rest = (1,2)

# nb
test_eq(tensor(array([1,2,3])), torch.tensor([1,2,3]))
test_eq(tensor(1,2,3), torch.tensor([1,2,3]))
