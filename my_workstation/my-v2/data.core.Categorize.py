from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import show_titled_image, get_image_files, GrandparentSplitter, ImageItem, parent_label
from PIL import Image

# ## Categorize -
# export
class Categorize(Transform):
    """
    "Reversible transform of category string to `vocab` id"

    purpose:
    - how to do category transformation for labels?
    - of course, need to create a subclass of Transform
    - it has its own __init__, encodes, decodes, setups
    1. __init__(self, vocab, train_attr, subset_idx, mask, is_tuple):
        1.0 inherit and introduce unique attributes for `Categorize`
        1.1 `self.vocab`, `self.train_attr`, `self.subset_idx`
        1.2 `self.o2i` is derived from `self.vocab`
    2. setups(self, dsrc):
        2.1 during the setup period, prepare self.vocab, self.o2i from `dsrc` with `self.train_attr` or `self.subset_idx`
    3. encodes(self, o):
        3.1 from unique cateory to idx, return idx
        3.2 or just return the category
    4. decodes(self, o):
        4.1 return self.vocab[o]
    """
    order,assoc=1,Item
    def __init__(self, vocab=None, train_attr="train", subset_idx=None, mask=None, is_tuple=None):
        super().__init__(mask=mask,is_tuple=is_tuple)
        self.vocab,self.train_attr,self.subset_idx = vocab,train_attr,subset_idx
        self.o2i = None if vocab is None else {v:k for k,v in enumerate(vocab)}

    def setups(self, dsrc):
        if not dsrc: return
        if self.subset_idx is not None: dsrc = dsrc.subset(self.subset_idx)
        elif self.train_attr: dsrc = getattr(dsrc,self.train_attr)
        self.vocab,self.o2i = uniqueify(dsrc, sort=True, bidir=True)

    def encodes(self, o): return self.o2i[o] if self.o2i else o
    def decodes(self, o):  return self.vocab[o]
# ### End-to-end dataset example with MNIST
path = untar_data(URLs.MNIST_TINY)
(path/'train').ls()
items = get_image_files(path)
splitter = GrandparentSplitter()
splits = splitter(items)
train,valid = (items[i] for i in splits)
train,valid
timg = Transform(Image.open, # encodes
        assoc=ImageItem(cmap="Greys", figsize=(1,1)))# assoc=Item no more
timg2tensor = Transform(compose(array,tensor))# this tfm is array+tensor
tfms = [[timg,timg2tensor,partial(torch.unsqueeze,dim=0)],# group tfms 1 for x
        [parent_label, Categorize(subset_idx=splits[0])]] # group tfms 2 for y


# important! how to understand TfmOver.piped and TfmdList(items, tfm)
tfm = TfmOver.piped(tfms)
# this func created `a`, the duplicate Transform, so that when an item go through this tfm, it returns two copies
# a = [functools.partial(<function replicate at 0x1258e4bf8>, match=(#2) [(#3) [<function open at 0x122cf8048>,<function compose.<locals>._inner at 0x125820378>,functools.partial(<built-in method unsqueeze of type object at 0x113876950>, dim=0)], (#2) [<function parent_label at 0x1259180d0>,<class '__main__.Categorize'>]]),
# then this func turn `tfms` into `TfmOver`, i.e., make 2 pipelines from `tfms`
# b = TfmOver((#2) [[],[]])]}
# finally wrap a, b into a single pipeline, so that they linked in order

# so that when `TfmdList(items, tfm)`, it is to bind items to tfm and set up tfm ready to use, so that datasets[0] can actually apply tfm to items[0]
# 0. to setup all pipelines and Transforms, will do the following
# 1. set up a, so when `items[0]` it outputs two copies of items[0]
# 2. start to set up b => set up b[0] => TfmOver.setup to Transform.setup to Pipeline.setups to Pipeline.add to loop through and set up each tfm inside b[0], at the end, `items[0]` can do transforms from image to tensor =>  set up b[1] => TfmOver.setup to Transform.setup to Pipeline.setups to Pipeline.add to loop through and set up each tfm inside b[1], at the end, `items[1]` can do transforms from image to label, meanwhile, `Categorize.setups` get `self.vocab` and `self.o2i` ready based on `items` and `subset_idx`
# 3. apply each pipeline to each copy
datasets = TfmdList(items, tfm)

# it will zip two copies of items[0] with two pipelines from b
# TfmOver.__call__ will do this zip work
datasets[0]
# NB: `DataSource` is an easier way to handle this common case
train_ds,valid_ds = map(datasets.subset, splits)

x,y = train_ds[3]
xd,yd = train_ds.decode_at(3)
test_eq(parent_label(train[3]),yd)
test_eq(array(Image.open(train[3])),xd[0])

train_ds.show_at(3);
