from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files, get_image_files
# ### Show
# %%
#export
def show_image(im, ax=None, figsize=None, title=None, ctx=None, **kwargs):
    """
    "Show a PIL image on `ax`."

    purpose:
    - How do we turn tensors into images?
    - How to put everything about plotting under control? How to use it?
        a. first args: `im` = tensor
        b. canvas args: `ax` or `ctx`? but could be None most of time
        c. figsize args: `figsize`, usually (5,8) alike
        d. title
        e. **kwargs: like `cmap='Greys'`
    - use `shape[0]<5` to control whether do permutation or not

    steps:
    1. we need to do the usual `_,ax = plt.subplots(figsize=figsize)`
    2. usually we deal with tensor, put it on cpu,
    2. put first dim last, handles permutation automatically
    3. if a single channel tensor, then treat it as a 2d tensor
    4. `ax.imshow` to plot image from tensor
    5. add title and `axis` off
    """
    ax = ifnone(ax,ctx)
    if ax is None: _,ax = plt.subplots(figsize=figsize)
    # Handle pytorch axis order
    if isinstance(im,Tensor):
        im = to_cpu(im)
        if im.shape[0]<5: im=im.permute(1,2,0)
    # Handle 1-channel images
    if im.shape[-1]==1: im=im[...,0]
    ax.imshow(im, **kwargs)
    if title is not None: ax.set_title(title)
    ax.axis('off')
    return ax

# `show_image` can show b&w images...
im = make_cross_image() # default black and white
ax = show_image(im, cmap="Greys", figsize=(2,2)) # cmap='Greys' is from kwargs

# ...and color images with standard `c*h*w` dim order...

im2 = make_cross_image(False)
ax = show_image(im2, figsize=(2,2))

# ...and color images with `h*w*c` dim order...

im3 = im2.permute(1,2,0)
ax = show_image(im3, figsize=(2,2))
# %%
show_title("Cross", ax)
ax = show_image(im, cmap="Greys", figsize=(2,2), title="cross")
