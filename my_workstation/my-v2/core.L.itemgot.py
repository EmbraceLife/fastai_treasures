from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

t = L([[1,2,3],[4,5,6]]); t
t.itemgot(1)
t = L([tensor(1,2,3), tensor(4,5,6)]); t
t.itemgot(2)
