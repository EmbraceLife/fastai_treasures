from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import show_titled_image

im = make_cross_image() # default black and white
im2 = make_cross_image(False)
im3 = im2.permute(1,2,0)

#export
class ImageItem:
    "An item that `show`s with `show_image`"
    def __init__(self, **kwargs): self.kw = kwargs
    def show(self, o, ctx=None, **kwargs): return show_image(o, ax=ctx, **{**kwargs,**self.kw})


ii = ImageItem(title='this is im', cmap='Greys')
ii.show(im)
ii = ImageItem(title='this is im2')
ii.show(im2)


#export
class TitledImageItem:
    "An item that `show`s an (image,title) tuple with `show_titled_image`"
    def __init__(self, **kwargs): self.kw = kwargs
    def show(self, o, ctx=None, **kwargs): return show_titled_image(o, ax=ctx, **{**kwargs,**self.kw})
# %% markdown

tii = TitledImageItem(cmap='Greys')
tii.show((im, "this is im"))
tii = TitledImageItem()
tii.show((im3, "this is im3")) # permutation is not allowed due to `shape[0] <5`
