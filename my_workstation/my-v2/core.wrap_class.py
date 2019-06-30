from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import *

def bar1(self, x): return x+2 # add methods before @wrap_class
bar2 = lambda self, x: self.a + x # self is usually added
@wrap_class('_P', 'alpha', a=2, bar1=bar1, bar2=bar2) # add methods in decorator
def bar(self,x): return x+1 # add methods after decorator
t = _P(100, b='new attr', c=int); t # 100 assigned to 'alpha'
