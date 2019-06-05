from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import add_docs

################
# not_finished: docs is not finished properly by official source yet
def docs(cls):
    "Decorator version of `add_docs"
    add_docs(cls, **cls._docs)
    return cls

class _T:
    def f(self): pass
    @classmethod
    def g(cls): pass

##################
# not an example of `docs`
add_docs(_T, "a", f="f", g="g")

test_eq(_T.__doc__, "a")
test_eq(_T.f.__doc__, "f")
test_eq(_T.g.__doc__, "g")
