from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import *

@patch
def __repr__(cls:TfmdList):
    """
    purpose:
    - what should we look at when print out the `TfmdList` object?
    - to know everything, we could print out:
        1. class name,
        2. `cls.items`,
        3. `cls.tfm`
    - `cls.tfm` is to use `Pipeline.__repr__` to display
    """
    return f"{cls.__class__.__name__}: {cls.items}\ntfms - {cls.tfm}"

show_doc(TfmdList.__repr__)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int)
pipe = Pipeline([negtfm(),floattfm()])
tl = TfmdList([1,2,3], pipe, do_setup=True)
tl
tl.tfm
