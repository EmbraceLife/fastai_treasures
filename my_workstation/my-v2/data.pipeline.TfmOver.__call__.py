from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
###############################################################
from local.data.pipeline import *



@patch
def __call__(cls:TfmOver, o, *args, **kwargs):
    """
    oneliner:
    - "List of output of each of `tfms` on `o`"

    purpose:
    - what we want to achieve with `TfmOver.__call__(o)`?
    - we know, `Pipeline.__call__(o)`, is to let every `Transform` or `TfmOver` inside do `__call__` on `o`
    - we know `Transform.__call__(o)` is to apply `encodes` onto `o`
    - so how much different should `TfmOver.__call__(o)` be?
    - most use cases, `TfmOver.tfm` is a list of pipelines, and
    - `o` has the same amount of duplicate elements as the length of pipeline list
    - we zip `o` and `TfmOver.tfms`, and apply each pipeline on each duplicate of `o`
    - put all transformation results inside a list and return the list
    """
    ####################
    # official source
    # if cls.activ is not None: return cls.tfms[cls.activ](o[cls.activ], *args, **kwargs)
    # return [t(p, *args, **kwargs) for p,t in zip(o,cls.tfms)]

    if cls.activ is not None:
        p = cls.tfms[cls.activ]
        i = o[cls.activ]
        return p(i, *args, **kwargs)

    res = []
    for p,t in zip(o,cls.tfms):
        res.append(t(p, *args, **kwargs))
    return res

############ simple example
TfmOver.__call__
# can't do `doc(TfmOver.__call__)` here
tp = TfmOver(tfms=[[operator.neg, float], [operator.neg]])
tp.setups()
tp([3,3])

############# complex example see class Categorize example
from local.data.external import *
from local.data.core import *
from PIL import Image


path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
items = get_image_files(path)
timg = Transform(Image.open, # encodes
        assoc=ImageItem(cmap="Greys", figsize=(1,1)))# assoc=Item no more
timg2tensor = Transform(compose(array,tensor))# this tfm is array+tensor
tfms = [[timg,timg2tensor,partial(torch.unsqueeze,dim=0)],# group tfms 1 for x
        [parent_label, Categorize(subset_idx=splits[0])]] # group tfms 2 for y

# show_doc(TfmOver.__init__)
to = TfmOver(tfms)
# show_doc(TfmOver.__call__)
o = [items[0], items[0]]
# always remember to do setups()
to.setups()
to(o)
