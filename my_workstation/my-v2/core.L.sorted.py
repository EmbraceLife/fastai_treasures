from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

###############################################################################
###############################################################################
# python default `sorted` is good
t = [1,2,3]
hasattr(t, 'sorted')
sorted(t, reverse=True) # only use builtin sorted

# del L.sorted
t = L(1,2,3);t
hasattr(t, 'sorted')
hasattr(t, 'sorted')
t.sorted()
t = L('1','2','3')
t.sorted()
t = L('a','b','c')
t.sorted()

###############################################################################

@patch
def sorted(cls:L, key=None, reverse=False):
    """
    "New `L` sorted by `key`. If key is str then use `attrgetter`. If key is int then use `itemgetter`."

    why L.sorted?
    - we want `L.sorted()` to do the same as the builtin `sorted()`
    -
    1. we want to sort more complex L such as a L of transforms
    2. different transforms have different values for property `order`
    3. we want to use the values of `order` to sort L of transforms
    """
    if isinstance(key,str):   k=lambda o:getattr(o,key,0)
    elif isinstance(key,int): k=itemgetter(key)
    else: k=key
    return L(sorted(cls.items, key=k, reverse=reverse))
##############################simple example
t = L(3,1,2);t
hasattr(t, 'sorted')
hasattr(t, 'sorted')
t.sorted()
t = L('1','2','3')
t.sorted(reverse=True)
t = L('a','b','c')
t.sorted(reverse=True)

############### more complex example, with the use of 'order'
class _Tfm():
    def __init__(self, order=None, items=None):
        self.order = order
t1=_Tfm(1)
t1.order
t2=_Tfm(2)
t2.order
L(t2,t1)
L(t1,t2).sorted(key='order')
L(t1,t2).sorted(key='order', reverse=True)
