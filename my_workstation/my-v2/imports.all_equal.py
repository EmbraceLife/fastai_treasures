import itertools
from torch import Tensor
import torch, numpy as np, operator
from numpy import array,ndarray
from typing import Iterable,Iterator, Generator

######################
# ever think of using one function to compare all sorts of types?
def equals(a,b):
    "Compares `a` and `b` for equality; supports sublists, tensors and arrays too"
    cmp = (torch.equal    if isinstance(a, Tensor  ) and a.dim() else
           np.array_equal if isinstance(a, ndarray ) else
           operator.eq    if isinstance(a, str     ) else
           all_equal      if isinstance(a, (list,tuple,Generator,Iterator)) else
           operator.eq)
    return cmp(a,b)

equals(range(3), range(3))
equals([1],[1])

######################
# compare both length and values
def all_equal(a,b):
    "Compares whether `a` and `b` are the same length and have the same contents"
    return all(equals(a_,b_) for a_,b_ in itertools.zip_longest(a,b))

a = [1,2,3]
b = [1,2,3]
all_equal(a, b)
a = [1,2,3]
b = [1,1,2,3]
all_equal(a, b)
