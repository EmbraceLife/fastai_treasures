from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test

#####################
# nequals = test on a and b equal or not
# a, b = single value or list
# output = true, equal
# output = false, equal?

def nequals(a,b):
    "Compares `a` and `b` for `not equals`"
    return not equals(a,b)

def example()
    nequals(['abc'], ['ab'])
    nequals(['abc'], ['abc'])
    test_fail(lambda: nequals(['abc'], ['abc' ]))

def inspection()
    sig(test)
