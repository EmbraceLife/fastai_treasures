from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
###############################################################
from local.data.pipeline import *


@patch
def __repr__(cls:TfmOver):
    """
    purpose:
    - when printing `TfmOver`, we just want to see all the pipelines
    - Note: always `setups()` first
    """
    return f'TfmOver({cls.tfms})'

negtfm = Transform(operator.neg,decodes = operator.neg)#, assoc=Item)
fltfm = Transform(float, decodes=int)
tp = TfmOver(tfms=[[negtfm, fltfm], [negtfm]])
tp.tfms
tp.setups()
tp
tp.tfms
