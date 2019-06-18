from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files, get_image_files



path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
t3 = get_files(path/'train'/'3', extensions='.png', recurse=False)
t7 = get_files(path/'train'/'7', extensions='.png', recurse=False)
t  = get_files(path/'train', extensions='.png', recurse=True)

items = [path/'train/3/9932.png', path/'valid/7/7189.png',
         path/'valid/7/7320.png', path/'train/7/9833.png',
         path/'train/3/7666.png', path/'valid/3/925.png',
         path/'train/7/724.png', path/'valid/3/93055.png']

# ### Label
# The final set of functions is used to *label* a single item of data.
# export
def parent_label(o, **kwargs):
    """
    "Label `item` with the parent folder name."

    purpose:
    - often files have their labels stored in their parent folders
    - so we extract their labels from their parent folders

    Note:
    - if item `o` is not a Path but a string,
    - then use `/` to split it and return the last element
    """
    return o.parent.name if isinstance(o, Path) else o.split(os.path.sep)[-1]

# Note that `parent_label` doesn't have anything customize, so it doesn't return a function - you can just use it directly.

test_eq(parent_label(items[0]), '3')
[parent_label(o) for o in items]

# export
def RegexLabeller(pat):
    """
    "Label `item` with regex `pat`."

    purpose
    - sometimes we want to use regular expression to search pattern from a long string
    - we make life easier with
        a. `RegexLabeller(path)` wrap the pattern inside `_inner` and return the `_inner`
        b. `_inner(o)` to process a single item `o` to search the pattern and return the found pattern in string

    Note:
    - problem: how to write the regex pattern
    - learn: https://regexr.com/ login with github account (e.g., lookup method)
    """
    pat = re.compile(pat)
    def _inner(o, **kwargs):
        res = pat.search(str(o))
        assert res,f'Failed to find "{pat}" in "{o}"'
        return res.group(1)
    return _inner

# `RegexLabeller` is a very flexible function since it handles any regex search of the stringified item. For instance, here's an example the replicates the previous `parent_label` results.

f = RegexLabeller(r'/(\d)/')
test_eq(parent_label(items[0]), '3')
[f(o) for o in items]
for o in items:
    f(o)
