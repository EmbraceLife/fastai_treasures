from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import *

@patch
def __repr__(cls:Pipeline):
    """
    "to print out all tfms"

    purpose:
    - how `cls.tfms` is created? what type is it?
    """
    return str(cls.tfms)

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg)
mk_class('floattfm', sup=Transform, encodes=float, decodes=int, assoc=Item)
neg = negtfm(is_tuple=True, mask=[True]*3, assoc=Item)
flt = floattfm(is_tuple=True, mask=[True]*3, assoc=None) # note: who has `assoc`
p = Pipeline([neg, flt])
p.tfms
p.setups()
p.tfms
p.tfms.__class__
