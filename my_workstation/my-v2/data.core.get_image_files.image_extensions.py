from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files
#export
"""
this is where we get all image extensions
"""
image_extensions = set(k for k,v in mimetypes.types_map.items() if v.startswith('image/'))
#export
def get_image_files(path, recurse=True, include=None):
    """
    "Get image files in `path` recursively."

    purpose:
    - `get_files` can help get any type files from deep subfolders
    - `get_image_files` does the same only for image files
    """
    return get_files(path, extensions=image_extensions, recurse=recurse, include=include)
# This is simply `get_files` called with a list of standard image extensions.
path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
t = get_files(path/'train', extensions='.png', recurse=True)
test_eq(len(t), len(get_image_files(path, recurse=True, include='train')))
