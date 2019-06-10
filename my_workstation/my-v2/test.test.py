from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail

### how to use assert ######
# def assert:
# assert False/None/0/0. "Error/Exception Rise with this message"
#####################

def test(a, b, cmp,cname=None):
    """
    `assert` that `cmp(a,b)`; display inputs and `cname or cmp.__name__` if it fails

    purpose:
    1. usually when we are doing test, we are compare `a` and `b`
        with some operations `cmp`;
    2. if `assert cmp(a,b)` without error/exception, then great
    3. if error/exception rises, send a message `f"{cname}:\n{a}\n{b}`
        to print out the operator name and the content of `a` and `b`

    steps:
    1. make sure to get the operator's name
    2. assert on the comparison otherwise send a message like above
    """
    if cname is None: cname=cmp.__name__
    assert cmp(a,b),f"{cname}:\n{a}\n{b}"


test([1,2],[1,2], operator.eq)
test_fail(lambda: test([1,2],[1], operator.eq))
test([1,2],[1],   operator.ne)
test_fail(lambda: test([1,2],[1,2], operator.ne))
show_doc(all_equal)
test(['abc'], ['abc'],  all_equal)
show_doc(equals)
test([['abc'],['a']], [['abc'],['a']],  equals)
