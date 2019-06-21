from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

@patch
def __repr__(cls:L):
    """
    why L.__repr__? because
    - we want to print out L nicely

    how to use L.__repr__?
    - just cmd+enter the L instance, like `L(1,2,3)`

    how L.__repr__ work?
    - we use `coll_repr` to print out L
    - the key step is `','.join(itertools.islice(map(str,c), max))`
    - `L.items` can get through `itertools.islice(map(str,c), max)`
    - `L.__getitem__` help get through `','.join(....)` 
    """
    return f'{coll_repr(cls)}'
###############################################################################
# now the new L.__repr__ can display L.items properly
t = L(range(100)); t
t.__repr__()
t[55]
