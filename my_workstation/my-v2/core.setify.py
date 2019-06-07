from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L

#################
# `setify(o)`
# = return o if o is a set
# = return a new set from `set(L(o))`

def setify(o): return o if isinstance(o,set) else set(L(o))

def examples():
    test_eq(setify(None),set())
    test_eq(setify('abc'),{'abc'})
    test_eq(setify([1,2,2]),{1,2})
    test_eq(setify(range(0,3)),{0,1,2})
    test_eq(setify({1,2}),{1,2})
