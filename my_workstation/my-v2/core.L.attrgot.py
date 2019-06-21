from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


###############################################################################
###############################################################################
@patch
def attrgot(cls:L, k):
    """
    why need L.attrgot(k)
    - if we a complex L which contains
        - multiple instances of a class
        - those instances share same attributes with different values
    - what if we want to access values of an attribute of all instances?
    - we want `t.attrgot('order')` do it for us

    how to use L.attrgot(k)
    - `t.attrgot(k)`
    - `t` is L instance with many instances of a class, e.g., '_Tfm'
    - `k` is an attribute name, e.g., 'order'
    """
    return cls.mapped(lambda o:getattr(o,k,0))
###############################################################################
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
attrgot(t, 'order')
