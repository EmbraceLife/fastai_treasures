from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

def to_np(x):
    "Convert a tensor to a numpy array."
    return x.data.cpu().numpy()

###############################################################################
def np_func(f):
    """
    purpose:
    1. we have lots of useful functions only dealing with arrays not tensors
    2. instead of rewriting them for tensors, why not use a decorator to make
        all of them work for tensors?
    3. this decorator can wrap around the array function to do two things:
        3.1 receiving tensors from outside and convert to arrays
        3.2 after array function done working, convert output back to tensor
    4. this way, tensor in, array function process, and tensor out

    Note: the way _inner or wrapper function only convert the positional arguments from tensor to array, not the named arguments
    """
    def _inner(*args, **kwargs):
        nargs = [to_np(arg) if isinstance(arg,Tensor) else arg for arg in args]
        return tensor(f(*nargs, **kwargs))
    functools.update_wrapper(_inner, f)
    return _inner

# This decorator is particularly useful for using numpy functions as fastai metrics, for instance:

from sklearn.metrics import f1_score

@np_func
def f1(inp,targ): return f1_score(targ, inp) # see only positional args

a1,a2 = array([0,1,1]),array([1,0,1])
t = f1(tensor(a1),tensor(a2));t # tensor in and tensor out
f1_score(a1,a2) # array in
show_doc(f1_score)
