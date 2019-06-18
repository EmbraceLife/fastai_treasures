from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files

# %% markdown
# It's often useful to be able to create functions with customized behavior. `fastai.data` generally uses functions named as CamelCase verbs ending in `er` to create these functions. `FileGetter` is a simple example of such a function creator.
# %%
#export
def FileGetter(suf='', extensions=None, recurse=True, include=None):
    """
    oneliner:
    - "Create `get_files` partial function that searches path suffix `suf` and passes along args"

    Purupose:
    - `get_files` has too many args to set in order to work
    - How can we make it easier to use by adjusting one arg instead?
    - use `FileGetter(...)` to set default for most args
    - use its returned _inner func to easily do `get_files` by adjusting a single arg `o`
    - in this case only adjust the directory to extract files from
    - the directory is final level as `suf` directory is made ''.
    """
    def _inner(o, extensions=extensions, recurse=recurse, include=include): return get_files(o/suf, extensions, recurse, include)
    return _inner



path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
t3 = get_files(path/'train'/'3', extensions='.png', recurse=False)
t7 = get_files(path/'train'/'7', extensions='.png', recurse=False)
t  = get_files(path/'train', extensions='.png', recurse=True)
fpng = FileGetter(extensions='.png', recurse=False)
test_eq(len(t7), len(fpng(path/'train'/'7')))
test_eq(len(t), len(fpng(path/'train', recurse=True)))
fpng_r = FileGetter(extensions='.png', recurse=True)
test_eq(len(t), len(fpng_r(path/'train')))
# %%
