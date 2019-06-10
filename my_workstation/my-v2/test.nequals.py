from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test

def nequals(a,b):
    "Once you got `equals`, `nequals` is natural to you"
    return not equals(a,b)


nequals(['abc'], ['ab'])
nequals(['abc'], ['abc'])
test_fail(lambda: nequals(['abc'], ['abc' ]))


sig(test)
