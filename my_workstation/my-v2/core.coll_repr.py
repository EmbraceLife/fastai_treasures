from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

def coll_repr(c, max=1000):
    "String repr of up to `max` items of (possibly lazy) collection `c`"
    return f'(#{len(c)}) [' + ','.join(itertools.islice(map(str,c), 10)) + ('...'
            if len(c)>10 else '') + ']'

# pdb
coll_repr(range(1000))
coll_repr(range(9))
coll_repr(torch.tensor([[1,2],[3,4]]), max=1000)
# notebook
test_eq(coll_repr(range(1000)), '(#1000) [0,1,2,3,4,5,6,7,8,9...]')
