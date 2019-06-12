from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L

def setify(o):
    """
    purpose:
    1. you may want to turn everything into a set
    2. if it is already a set, just return it
    3. if not, make it a L, then turn it to set
    """
    return o if isinstance(o,set) else set(L(o))

setify(None)
setify('abc')
setify([1,2,2])
setify(range(0,3))
setify({1,2})
