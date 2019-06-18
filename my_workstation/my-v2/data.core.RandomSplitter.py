from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files, get_image_files

# ### Split
# The next set of functions are used to *split* data
# into training and validation sets. The functions return two lists
# - a list of indices or masks for each of training and validation sets.
# export
def RandomSplitter(valid_pct=0.2, seed=None, **kwargs):
    """
    "Create function that splits `items` between train/val with `valid_pct` randomly."

    purpose:
    - like FileGetter, we want life easier for splitting data
    - RandomSplitter wraps args like `valid_pct`, `seed`, `**kwargs`
    - `_inner` wraps `o` the data, and `**kwargs`
    - `_inner` does the actual splitting work

    Note:
    1. _inner only returns rand_idxes for training and validation items
    2. _inner does not return actual items

    """
    def _inner(o, **kwargs):
        if seed is not None: torch.manual_seed(seed)
        rand_idx = L(int(i) for i in torch.randperm(len(o)))
        cut = int(valid_pct * len(o))
        return rand_idx[cut:],rand_idx[:cut]
    return _inner

src = list(range(30)); src
f = RandomSplitter(seed=42)
trn,val = f(src)
assert 0<len(trn)<len(src)
assert all(o not in val for o in trn)
test_eq(len(trn), len(src)-len(val))
# test random seed consistency
test_eq(f(src)[0], trn)
trn,val
# how to make use of the idx from RandomSplitter
src = L(list(range(100,130)));src
src[trn]
src[val]
