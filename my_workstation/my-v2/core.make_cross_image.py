from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

def make_cross_image(bw=True):
    """
    oneliner: how to create a tensor for black-white cross image or color make_cross_image

    purpose:
    1. to create an image of bw or color cross, we need a tensor first;
    2. by change values in the tensor to add pattern or color
    3. permutate to change the dim position of channels is essential in creating images

    Note: this is just for example usage I think
    """
    if bw:
        im = torch.zeros(5,5)
        im[2,:] = 1.
        im[:,2] = 1.
    else:
        im = torch.zeros(3,5,5)
        im[0,2,:] = 1.
        im[1,:,2] = 1.
    return im
make_cross_image()
plt.imshow(make_cross_image(), cmap="Greys");
make_cross_image(False)
make_cross_image(False).shape
make_cross_image(False).permute(1,2,0).shape
plt.imshow(make_cross_image(False).permute(1,2,0));
###########################################################################
# what does permute actually do to a tensor
show_doc(make_cross_image(False).permute)
make_cross_image(False)[0,:,:]
make_cross_image(False).permute(1,2,0)[:,:,0]
