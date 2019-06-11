from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *


def _listify(o):
    """
    purpose:
    1. sometimes, we would like everything to be a list,
        but `list()` won't work in many cases
    2. `list(None)` won't work, so we use `[]`
    3. if it is a list, let it be `o`
    4. `list(str|array|tensor)` will have strange outputs, so use `[o]` instead
    5. if `is_iter(o)` is True, `list(o)` is fine
    6. other cases, just make it a list `[o]`
    Note: use `[]` more than `list()`, as `list()` won't work properly
            in many cases below
    """
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, (str,np.ndarray,Tensor)): return [o]
    if is_iter(o): return list(o)
    return [o]

test_fail(lambda: list(None))
test_fail(lambda: list(tensor(3)))
_listify(tensor(3))
list('yes')
_listify('yes')
list(array([1,2,3]))
_listify(array([1,2,3]))
_listify(np.ndarray([1,2]))
list(tensor(1,2))
_listify(tensor(1,2))
_listify(None)
_listify([1,2])
_listify((1,3))
