from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
##########
# `mapper(f)`
# = map a func onto every input of an collection
# mapper(f) is a lambda on its own
# mapper(f)(data) is how we use it

def mapper(f):
    "Create a function that maps `f` over an input collection"
    return lambda o: [f(o_) for o_ in o]

def examples():
    func = mapper(lambda o:o*2)
    test_eq(func(range(3)),[0,2,4])
