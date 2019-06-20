from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *
from local.core import _listify

def _listify(o):
    """
    why need _listify?
    - sometimes, we would like everything to be a list
    - but `list()` won't work in many cases
    - this func makes sure everything turned into a list

    How to use _listify()?
    - put anything into _listify()
    - it returns you a list

    How does _listify work?
    - sometimes, we would like everything to be a list
        - if `o` is a list, just return `o`
        - if `is_iter(o)` is True, `list(o)` is fine
            - `o` is generator, or iterator
            - `o` can be a tuple in this case
    - but `list()` won't work in many cases
        - `list(None)` won't work, so we use `[]`
        - `list(str|array|tensor)` will have strange outputs, so use `[o]`
        - other cases, just put `[]` around`o`, i.e., `[o]`

    Note: use `[]` more than `list()`, as `list()` won't work properly
            in many cases below
    """
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, (str,np.ndarray,Tensor)): return [o]
    if is_iter(o): return list(o)
    return [o]

show_doc(_listify)
####### simple examples
test_fail(lambda: list(None))
test_fail(lambda: list(tensor(3)))
_listify(None)
_listify(tensor(3))
list('yes')
_listify('yes')
list(array([1,2,3]))
_listify(array([1,2,3]))
_listify(np.ndarray([1,2]))
list(tensor(1,2))
_listify(tensor(1,2))
_listify([1,2])
_listify((1,3))
_listify(range(10))
