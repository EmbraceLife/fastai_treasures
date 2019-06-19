from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
###############################################################
from local.data.pipeline import *

@patch
def setups(cls:TfmOver, o=None):
    """
    oneliner:
    - "Setup each of `tfms` independently"

    purpose:
    - once we have a TfmOver with tfms turned into a list of pipelines,
    - we still need to get every pipeline setup for transformation
    - we use `cls.activ` to index each pipeline
    - after the setup, we put `cls.activ` back to None
    - normally after `setups()`, we can view tfms properly

    Note:
    - we don't do transformation with `TfmOver`
    - we don't really use `Pipeline` or `Transform` to do transformation on their own, but really do it through `TfmList`
    """
    for i,tfm in enumerate(cls.tfms):
        cls.activ = i
        tfm.setup(o)
    cls.activ=None

######### simple example
tp = TfmOver(tfms=[[operator.neg, float]])
doc(tp.setups)
tp.activ
tp.tfms
tp.tfms[0]._tfms[1].prev
tp.setups()
tp.tfms
isinstance(tp.tfms[0], Pipeline)
tp.tfms[0]
tp.tfms[0].tfms[1].prev
tp.assoc
######### more complex examples
mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('flttfm',   sup=Transform, encodes=float, decodes=int)
tp = TfmOver(tfms=[[negtfm(), flttfm()],[negtfm()]])
tp.tfms
tp.setups()
tp.tfms
tp.assoc
tp.xt
tp.yt

######
p = tp.piped(tp.tfms)
p.tfms
p._tfms
