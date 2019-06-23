from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


get_class
mk_class
wrap_class


@wrap_class('T', a=2)
def bar(self,x): return x+1

t = T(b='new attr', c=int)
T
module(T)
