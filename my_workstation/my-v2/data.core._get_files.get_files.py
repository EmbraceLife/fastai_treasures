#default_exp data.core
#export
from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
# Not exported since we only use it for examples
from PIL import Image
# # Helper functions for processing data
# > Functions for getting, splitting, and labeling data, etc
# ## Get, split, label, and show
# For most data source creation we need functions to get a list of items,
# split them in to train/valid sets, and label them.
# fastai provides functions to make each of these steps
# easy (especially when combined with `fastai.data.blocks`),
# along with showing data (we'll only define image showing in this section).
# ### Get
# First we'll look at functions that *get* a list of items (generally file names).
# We'll use *tiny MNIST* (a subset of MNIST with just two classes,
# `7`s and `3`s) for our examples/tests throughout this page.
path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
##############################################################################
############################# experiment source ##############################
# export
def _get_files(p, fs, extensions=None):
    """
    purpose:
    - with `get_files`, we can go to specified subfolders
    - and access all files within each subfolder
    - BUT how shall we filter out the files from all the files in the subfolder?
    - we will loop through each file, and ignore hidden files,
    - and ignore files' suffixes don't match `extensions`
    - put all the remaining files in their proper path objects,
    - and put them into a list `res`
    - return such as list
    """
    p = Path(p)
    res = []
    for f in fs:
        if not f.startswith('.') and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions):
            res.append(p/f)
    # res = [p/f for f in fs if not f.startswith('.')
           # and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions)]
    return res

# export
def get_files(path, extensions=None, recurse=True, include=None):
    """
    "Get all the files in `path` with optional `extensions`, optionally with `recurse`."

    purpose:
    - all data files are in folders, level by level downward
    - need to get them out and reside onto a single level
    - set `recurse=True` to go down each subfolder, get files out
    - if `recurse=False`, only extract files from immediate folder(not its subfolders)
    - to `include` a list of subfolders for exclusive selection
    - use `extensions` to list suffixes of files to extract
    - of course, by default, `.`hidden files won't be extracted
    - finally return all the files in path objects inside a L object

    Note:
    - d[:] = tep vs d = tep huge difference?! important!
    """
    path = Path(path)
    extensions = setify(extensions)
    extensions = {e.lower() for e in extensions}
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path)): # returns (dirpath, dirnames, filenames)
            if include is not None and i==0:
                # important!
                # d[:] = [o for o in d if o in include] # official
                # d = [o for o in d if o in include] # not working
                tep = []
                for o in d:
                    if o in include:
                        tep.append(o)
                d[:] = tep # important! working
                # d = tep # not working
            else:
                # d[:] = [o for o in d if not o.startswith('.')]
                tep = []
                for o in d:
                    if not o.startswith('.'):
                        tep.append(o)
                d[:] = tep

            res += _get_files(p, f, extensions)
    else:
        # f = [o.name for o in os.scandir(path) if o.is_file()]
        f = []
        for o in os.scandir(path):
            if o.is_file():
                f.append(o.name)

        res = _get_files(path, f, extensions)

    return L(res)
# This is the most general way to grab a bunch of file names from disk.
# If you pass `extensions` (including the `.`)
# then returned file names are filtered by that list.
# Only those files directly in `path` are included,
# unless you pass `recurse`,
# in which case all child folders are also searched recursively.
# `include` is an optional list of directories to limit the search to.
# %%
t3 = get_files(path=path/'train'/'3', extensions='.png', recurse=False)
t7 = get_files(path/'train'/'7', extensions='.png', recurse=False)
t  = get_files(path/'train', extensions='.png', recurse=True)
test_eq(len(t), len(t3)+len(t7))
test_eq(len(get_files(path/'train'/'3', extensions='.jpg', recurse=False)),0)
test_eq(len(t), len(get_files(path, extensions='.png', recurse=True, include=['train'])))
test_eq(len(t3), len(get_files(path/'train', extensions='.png', recurse=True, include='3')))
get_files(path/'train', extensions='.png', recurse=True, include='3')
t
# %%
#hide
test_eq(len(get_files(path/'train'/'3', recurse=False)),346)
test_eq(len(get_files(path, extensions='.png', recurse=True, include=['train', 'test'])),729)
# %% markdown
# It's often useful to be able to create functions with
# customized behavior. `fastai.data` generally uses functions
# named as CamelCase verbs ending in `er` to create these
# functions. `FileGetter` is a simple example of such a
# function creator.

##############################################################################
############################# original source ##############################
##############################################################################
# export
def _get_files(p, fs, extensions=None):
    p = Path(p)
    res = [p/f for f in fs if not f.startswith('.')
           and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions)]
    return res

# export
def get_files(path, extensions=None, recurse=True, include=None):
    "Get all the files in `path` with optional `extensions`, optionally with `recurse`."
    path = Path(path)
    extensions = setify(extensions)
    extensions = {e.lower() for e in extensions}
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path)): # returns (dirpath, dirnames, filenames)
            if include is not None and i==0: d[:] = [o for o in d if o in include]
            else:                            d[:] = [o for o in d if not o.startswith('.')]
            res += _get_files(p, f, extensions)
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_files(path, f, extensions)
    return L(res)
t3 = get_files(path/'train'/'3', extensions='.png', recurse=False)
t7 = get_files(path/'train'/'7', extensions='.png', recurse=False)
t  = get_files(path/'train', extensions='.png', recurse=True)
test_eq(len(t), len(t3)+len(t7))
test_eq(len(get_files(path/'train'/'3', extensions='.jpg', recurse=False)),0)
test_eq(len(t), len(get_files(path, extensions='.png', recurse=True, include='train')))
t
#hide
test_eq(len(get_files(path/'train'/'3', recurse=False)),346)
test_eq(len(get_files(path, extensions='.png', recurse=True, include=['train', 'test'])),729)
