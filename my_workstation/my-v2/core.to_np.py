from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import tensor

def to_np(x):
    """
    purpose:
    1. tensor and array are the most useful things
    2. we want to convert from tensor to array at ease
    3. as from array to tensor is as easy as `tensor(array([1,2,3]))`
    """
    return x.data.cpu().numpy()

t = tensor(array([1,2,3])); t
t3 = tensor(1,2,3); t3
t3 = to_np(t3)
type(t3)
t3
