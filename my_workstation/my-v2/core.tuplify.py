from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L, tensor

L(None)
tuplify(None, use_list=False, match=None)
t = L([1,2,3]); t
t = tuplify(t, use_list=False, match=None);t
t = tuplify(t, use_list=True, match=None);t
t = tuplify([1], use_list=True, match=[1,2,3]);t
