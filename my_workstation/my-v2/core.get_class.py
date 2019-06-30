from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import *

# bar_attr is not a method, but an attr to the object
_t = get_class('_t', 'a'); _t
t = _t(b='yes', bar_attr=lambda x: x+1);t 
t.bar_attr(5)


# bar_method is taken as a named argument, 
# it becomes a real method to the class, 
_t = get_class('_t', 'a', bar_method=lambda self, x: x+self.a); _t
t1 = _t(5, b='yes');t1 
t1.bar_method(5)

