from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files, get_image_files


#export
def ImageGetter(suf='', recurse=True, include=None):
    "Create `get_image_files` partial function that searches path suffix `suf` and passes along `kwargs`"
    def _inner(o, recurse=recurse, include=include): return get_image_files(o/suf, recurse, include)
    return _inner

# Same as `FileGetter`, but for image extensions.
path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
t = get_files(path/'train', extensions='.png', recurse=True)
test_eq(len(get_files(path/'train', extensions='.png', recurse=True, include='3')),
        len(ImageGetter(  'train',                    recurse=True, include='3')(path)))
