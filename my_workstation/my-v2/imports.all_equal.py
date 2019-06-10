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

def exercise1():
    equals(range(3), range(3))
    equals([1],[1])

######################
# compare both length and values
def all_equal(a,b):
    """
    purpose:
    - sometimes, we just want to be able to compare two items `a`, `b`
    - not only on values, but also the length, in case they are plural
    """
    return all(equals(a_,b_) for a_,b_ in itertools.zip_longest(a,b))

def exercise2():
    a = [1,2,3]
    b = [1,2,3]
    all_equal(a, b)
    a = [1,2,3]
    b = [1,1,2,3]
    all_equal(a, b)
