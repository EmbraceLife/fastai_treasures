from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

# turn everything into a list
def _listify(o):
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, (str,np.ndarray,Tensor)): return [o]
    if is_iter(o): return list(o)
    return [o]

# pdb
_listify(None)
_listify([1,2])
_listify('yes')
_listify(np.array([1,2]))
_listify(np.ndarray([1,2]))
_listify(torch.tensor([1,2]))
_listify(tensor(1,2))
