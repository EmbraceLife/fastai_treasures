from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


class _Tfm():
    def __init__(self, order=None, items=None):
        self.order = order
t1=_Tfm(1)
t1.order
t2=_Tfm(2)
t2.order
hasattr(t1, 'order')
t = L(t1, t2)
t.attrgot('order')

