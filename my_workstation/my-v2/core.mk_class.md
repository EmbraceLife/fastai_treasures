
from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc
from local.core import *

show_doc(mk_class)# check latest source and test

def foo(self): return 1
mk_class('_t', 'a', sup=GetAttr, doc='test doc', funcs=foo)
t = _t(3, b=2, _xtra=['lower'], default="GDP");t # __init__ 
t
# t. tab to see all attributes
```

# Oneliner
- Create a class using `get_class` and add to the caller's module"

# why mk_class(...)
- `get_class(...)` can create a new class with specified attrs for us
- but what if we want to add this class onto the caller's module
- we use `mk_class` to create and add onto module altogether

# how to use mk_class(...)
- the same as get_class(...)
- but does not return anything

# how to achieve it?
- `mod = inspect.currentframe().f_back.f_locals`

# Note:
- get_class(...) returns a new class
- new class is added onto local.core
- for some reason, `t.__repr__` and `_t.__repr__` is not the one defined in `get_class` but the builtin `__repr__`
- so, just use `wrap_class` or `get_class`, not `mk_class`

# Source Code
```python
def mk_class(nm, *fld_names, sup=None, doc=None, funcs=None, mod=None, **flds):
    
    "Create a class using `get_class` and add to the caller's module"
    if mod is None: mod = inspect.currentframe().f_back.f_locals
    res = get_class(nm, *fld_names, sup=sup, doc=doc, funcs=funcs, **flds)
    mod[nm] = res
    
File:      ~/Documents/doc-v2/dev/local/core.py
Type:      function
```
