from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

################
# `show_title(o, ax=None, ctx=None)`
# = to set title `o` for ax plot
# = or just print out the title `o` if `ax` is None 


def show_title(o, ax=None, ctx=None):
    "Set title of `ax` to `o`, or print `o` if `ax` is `None`"
    ax = ifnone(ax,ctx)
    if ax is None: print(o)
    else: ax.set_title(o)
