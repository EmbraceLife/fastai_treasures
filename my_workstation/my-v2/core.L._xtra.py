from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


show_doc(L._xtra)
# L._xtra is a property defined inside the class
# we can define it outside the class too
L._xtra =  property(lambda x: [o for o in dir(list) if not o.startswith('_')])

# example
t = L(1,2,3); t

t._xtra
