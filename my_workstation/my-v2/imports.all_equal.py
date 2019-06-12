import itertools
from torch import Tensor
import torch, numpy as np, operator
from numpy import array,ndarray
from typing import Iterable,Iterator, Generator
from local.test import *
from local.notebook.showdoc import show_doc
##### how to use all() #################
# def all((True, True))

def all_equal(a,b):
    """
    purpose:
    0. often we compare whether scalar `a` and `b` for equality, but
    1. sometimes, we have to compare every value between `a` and `b`
        they are two lists, tuples, generators, or iterators!
    2. therefore, we need `itertools` to help pair them for comparison
    3. then `a_`, `b_` can be any type even still lists, ....
    4. therefore, we need the almighty `equals` to compare them all

    steps:
    1. use `itertools.zip_longest` to pair every value between `a` and `b`
        together
    2. use almighty `equals` to compare `a_` and `b_`
    3. use `all(...)` to find out whether any pair is not equal.
    4. return True if every pair of values equal, otherwise False

    Notes:
    1. a, b have to be iterable
    """
    return all(equals(a_,b_) for a_,b_ in itertools.zip_longest(a,b))

def equals(a,b):
    """
    "Compares `a` and `b` for equality; supports sublists, tensors and arrays too"

    purpose:
    1. equality is probably what we test/compare the most
    2. we would like to be able to compare equality on all types including
        `Tensor, ndarray, string, list, tuple, Generator, Iterator`
    3. as output, True for equal, False for not

    steps:
    1. if `a` is a tensor with dim >= 1, `cmp = torch.equal`
    2. if `a` is a `ndarray`, `cmp = np.array_equal`
    3. if `a` is a `str`, `cmp = operator.eq`
    4. if `a` is any of `(list, tuple, Generator, Iterator)`, `cmp = all_equal`
    5. else `cmp = operator.eq`
    """
    cmp = (torch.equal    if isinstance(a, Tensor  ) and a.dim() else
           np.array_equal if isinstance(a, ndarray ) else
           operator.eq    if isinstance(a, str     ) else
           all_equal      if isinstance(a, (list,tuple,Generator,Iterator)) else
           operator.eq)
    return cmp(a,b)

# a, b must be iterable
show_doc(itertools.zip_longest) # expect a, b to be iterable
test_fail(lambda: all_equal(1, 2), msg='should fail', contains='iteration')
# what are iterables
equals(range(3), range(3))
equals([1],[1])
a = [1,2,3]
b = [1,2,3]
all_equal(a, b)
a = [1,2,3]
b = [1,1,2,3]
all_equal(a, b)
