from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

##################
# `Item()`
# = a class with a single function `show(o, ctx=None, **kwargs)`
# = which does the same job as `show_title`,
# = finally returns `ctx` or the actual `ax`

class Item():
    "An item that displays text (for `Transform.assoc`)"
    def show(o, ctx=None, **kwargs):
        show_title(o, ctx, **kwargs)
        return ctx
