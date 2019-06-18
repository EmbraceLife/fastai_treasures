from local.imports import *
from local.test import *
from local.core import *
from local.data.pipeline import *
from local.data.external import *
from local.notebook.showdoc import show_doc
from local.data.core import get_files, get_image_files, show_image

#export
def show_titled_image(o, **kwargs):
    """
    purpose:
    - we often have a data sample as (x, y)
    - how to plot x and having y as title?

    oneliner:
    - "Call `show_image` destructuring `o` to `(img,title)`"
    """
    show_image(o[0], title=str(o[1]), **kwargs)

#export
def show_image_batch(b, show=show_titled_image, items=9, cols=3, figsize=None, **kwargs):
    """
    "Display batch `b` in a grid of size `items` with `cols` width"

    purpose:
    - `show_image` and `show_titled_image` are dealing with a single image
    - so, how to plot a batch of (x,y)s?
    - what if we want to constrain the subplots to be specific cols?
    - e.g., `items=8`, 8 subplots are required to be plotted,
        - then how many rows of the fig should be there?
    - `b` is a batch of x and a batch of y in a tuple

    steps:
    1. use algo on `items` and `cols` to calc number of rows
    2. set the default `figsize`
    3. create empty subplots and fig based on `cols`, `rows`, `figsize`
    4. zip x, y ax properly for subplots

    note: important!
    - `for *o,ax in zip(*to_cpu(b), axs.flatten()):` =>
    - `for (x,y), ax in zip((to_cpu(b[0]), to_cpu(b[1])), axs.flatten())`
    - `items` working with `cols` has nothing to do with batch_size
    """
    rows = (items+cols-1) // cols
    if figsize is None: figsize = (cols*3, rows*3)
    fig,axs = plt.subplots(rows, cols, figsize=figsize)
    # for *o,ax in zip(*to_cpu(b), axs.flatten()): show(o, ax=ax, **kwargs)
    for *o,ax in zip(*to_cpu(b), axs.flatten()):
        show(o, ax=ax, **kwargs)

im = make_cross_image() # default black and white
im2 = make_cross_image(False)
im3 = im2.permute(1,2,0)
show_image_batch(([im,im2,im3],['bw','chw','hwc']), items=8)
