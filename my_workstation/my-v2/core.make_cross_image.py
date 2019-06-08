from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
####################
# `make_cross_image(bw=True)`
# `bw=True` = black and white cross image
# `bw=False` = color cross image
# Not sure of color image logic behind

def make_cross_image(bw=True):
    "Create a tensor containing a cross image, either `bw` (True) or color"
    if bw:
        im = torch.zeros(5,5)
        im[2,:] = 1.
        im[:,2] = 1.
    else:
        im = torch.zeros(3,5,5)
        im[0,2,:] = 1.
        im[1,:,2] = 1.
    return im
# %%
make_cross_image()
plt.imshow(make_cross_image(), cmap="Greys");
make_cross_image(False)
make_cross_image(False).permute(1,2,0)
plt.imshow(make_cross_image(False).permute(1,2,0));
