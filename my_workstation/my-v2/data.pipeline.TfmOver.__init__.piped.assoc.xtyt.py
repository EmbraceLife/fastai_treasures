from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
###############################################################
from local.data.pipeline import *

###############################################################
class TfmOver(Transform):
    """
    "Create tuple containing each of `tfms` applied to each of `o`"

    purpose:
    - why do we need `TfmOver` after `Pipeline`, `TfmdList`?
    0. sometimes, we want multiple pipelines to work together
    1. therefore, we want to store multiple pipelines together
    2. we want to present the effect of different pipelines
    """
    def __init__(self, tfms=None):
        """
        oneliner:
        - TfmOver.__init__ is to create and store a list of pipelines as its `tfms`

        purpose:
        - what should be inside `TfmOver`?
            1. we want `self.tfms`:
                1.1 turn a list of tfms into a L of `Pipeline`s
            2. we want `self.activ` to set something active or not
        """
        # official source
        # if tfms is None: tfms = [None]
        # self.activ,self.tfms = None,L(tfms).mapped(Pipeline)
        # show_doc(TfmOver.__init__) for current offical code

        # source_made_uncool
        if tfms is None:
            tfms = [None]
        self.activ = None
        self.tfms = L(tfms).mapped(Pipeline)

    @property
    def assoc(self):
        """
        purpose:
        - since `assoc` is responsible for displaying
        - we are interested to see whether each pipeline has an assoc
        - and what they are
        - we are using `L.attrgot('assoc')` to find this attr of all elements
        """
        return self.tfms.attrgot('assoc')

    @classmethod
    def piped(cls, tfms=None, final_tfms=None):
        """
        "`Pipeline` that duplicates input, then maps `TfmOver` over `tfms`, optionally followed by any `final_tfms`"

        purpose:
        - the goal of `TfmOver` is to set up or lay over Transform/pipelines upon each other
        - in order to let data files going through these layers of pipelines
        - and return (x, y) as outputs of pipeline transformations

        steps:
        0. this func returns a pipeline of tranforms
        1. the first layer, is a `Transform` is to replicate a datafile for `tfms` times;
        2. the second layer is a L of pipelines of `tfms` by `TfmOver(tfms)` matching the copies of datafile
        3. third layer, is optional, a list of tfms with `is_tuple = True`
        """
        tfms = L(ifnone(tfms,[None]))
        init_tfm = partial(replicate,match=tfms)
        return Pipeline([init_tfm,cls(tfms)] + _set_tupled(final_tfms))

    # nicely return tfms for x and tfms for y
    xt,yt = add_props(lambda i,x:x.tfms[i])

mk_class('negtfm',   sup=Transform, encodes=operator.neg, decodes=operator.neg, assoc=Item)
mk_class('flttfm',   sup=Transform, encodes=float, decodes=int)
tp = TfmOver(tfms=[[negtfm(), flttfm()],[negtfm()]])
tp.activ

###### proper examples of `assoc`, `xt, yt` see data.pipeline.TfmOver.setups.py
tp.tfms # not setup yet
tp.xt
tp.yt
# tp.assoc # need setups to work properly, but we don't have it yet, instead
tp.tfms[0]._tfms.attrgot('assoc')

###### examples on piped
p = tp.piped(tp.tfms)
p.tfms
p._tfms
