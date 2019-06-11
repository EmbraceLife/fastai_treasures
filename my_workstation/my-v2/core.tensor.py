from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc


def tensor(x, *rest):
    """
    purpose:
    1. ever want to do `tensor(1,2,3)` and return tensor([1, 2, 3])
    2. and use `torch.tensor` can deal with tuple and list (copies made)
    3. use `as_tensor` for tensor, ndarray (can avoid copies)
    4. also want tensor(0), tensor([]) both to return `tensor(0)`
    """
    if len(rest): x = (x,)+rest
    # Pytorch bug in dataloader using num_workers>0
    if isinstance(x, (tuple,list)) and len(x)==0: return tensor(0)
    res = torch.tensor(x) if isinstance(x, (tuple,list)) else as_tensor(x)
    if res.dtype is torch.int32:
        warn('Tensor is int32: upgrading to int64; for better performance use int64 input')
        return res.long()
    return res

tensor(1,2,3) # both torch.tensor and np.array can't do it!
tensor(0)
tensor([])
tensor(array((1,2,3)))
tensor((1,2,3))
tensor([1,2,3])
tensor([[1,2], [3,4], [5,6]])# nb
tensor(range(5))
