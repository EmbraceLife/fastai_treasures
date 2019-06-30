from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

t = L(([1,2,8],[3,4,9],[5,6,10]))
t.tensored()
t.stack(dim=0)
t.stack(dim=-1)
