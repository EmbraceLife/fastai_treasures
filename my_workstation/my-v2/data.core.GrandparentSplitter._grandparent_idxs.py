from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files, get_image_files

# export

def _grandparent_idxs(items, name):
    """
    purpose:
    - we have all the file items from folders of all levels
    - but we want only those with a specific grandparent folder
    - the reason why grandparent folder is parent folder is for category
    - only grandparent folder can be train/valid folders
    - a natural way to do it is to find the idxs for files from that folder
    - this func does exactly that!
        1. `mask2idxs` turns True/False to idxes
    """
    return mask2idxs(Path(o).parent.parent.name == name for o in items)

# export
def GrandparentSplitter(train_name='train', valid_name='valid'):
    """
    "Split `items` from the grand parent folder names (`train_name` and `valid_name`)."

    purpose:
    - sometimes, we have files hierarchy with `train` and `valid` subfolders
    - so to split extracted data based on these two subfolders,
    - is to get all the idxs for files from `train` subfolder
    - and get the idxs for files from `valid` subfolders
    - `_grandparent_idxs` can get all idxs exactly for a partcular grandparent-folder

    Note:
    - `GrandparentSplitter` return the _inner func, which returns idxs for
    - both train and valid files
    - so, it actually split the idxs not items
    """
    def _inner(o, **kwargs):
        return _grandparent_idxs(o, train_name),_grandparent_idxs(o, valid_name)
    return _inner


path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
t3 = get_files(path/'train'/'3', extensions='.png', recurse=False)
t7 = get_files(path/'train'/'7', extensions='.png', recurse=False)
t  = get_files(path/'train', extensions='.png', recurse=True)

items = [path/'train/3/9932.png', path/'valid/7/7189.png',
         path/'valid/7/7320.png', path/'train/7/9833.png',
         path/'train/3/7666.png', path/'valid/3/925.png',
         path/'train/7/724.png', path/'valid/3/93055.png']
splitter = GrandparentSplitter() # return _inner function for idxs
test_eq(splitter(items),[[0,3,4,6],[1,2,5,7]])
train_idx, valid_idx = splitter(items)
L(items)[train_idx]
L(items)[valid_idx]

########### complex example
path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
items = get_image_files(path);items
splitter = GrandparentSplitter()
splits = splitter(items)
train,valid = (items[i] for i in splits)
train,valid
