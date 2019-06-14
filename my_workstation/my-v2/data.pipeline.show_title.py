from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

def show_title(o, ax=None, ctx=None):
    """
    purpose:
    1. "Set title of `ax` to `o`, or print `o` if `ax` is `None`"
    2. `ax` and `ctx` seem used interchangeably
    """
    ax = ifnone(ax,ctx)
    if ax is None: print(o)
    else: ax.set_title(o)
