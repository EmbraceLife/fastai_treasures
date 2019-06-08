from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
###############

# `add_props(f, n=2)`
# = add properties to a class, `n` set for number of properties
# = properties difference are based on `i` from `i in range(n)`, and
# = `partial(f, i)` => if `f` is lambda then must have two args `x` and `i`

def add_props(f, n=2):
    "Create properties passing each of `range(n)` to f"
    return (property(partial(f,i)) for i in range(n))

def examples():

    class _T(): a,b = add_props(lambda i,x:i*2)

    t = _T()
    test_eq(t.a,0)
    test_eq(t.b,2)

    class _T(): a,b,c,d = add_props(lambda i,x:i*2, n=4)
    t = _T()
    test_eq(t.a,0)
    test_eq(t.b,2)
    test_eq(t.c,4)
    test_eq(t.d,6)
