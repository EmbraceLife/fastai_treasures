from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail

#####################
# test = to test on the use of the operator `cmp` on a and b
# a, b = single value or list
# cmp = operator function
# cname = just a string for name
# output = nothing, if no error
# output = cname, a and b, if error or exception raises

def test(a, b, cmp,cname=None):
    "`assert` that `cmp(a,b)`; display inputs and `cname or cmp.__name__` if it fails"
    if cname is None: cname=cmp.__name__
    assert cmp(a,b),f"{cname}:\n{a}\n{b}"

def on_operator.eq():
  test([1,2],[1,2], operator.eq)
  test_fail(lambda: test([1,2],[1], operator.eq))

def on_operator.ne():
  test([1,2],[1],   operator.ne)
  test_fail(lambda: test([1,2],[1,2], operator.ne))

def on_all_equal():
  show_doc(all_equal)
  test(['abc'], ['abc'],  all_equal)

def on_equals():
  show_doc(equals)
  test([['abc'],['a']], [['abc'],['a']],  equals)
