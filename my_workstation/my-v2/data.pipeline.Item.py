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
    """
    purpose:
    1. it is designed for display text for `Transform.assoc`
    2. it is a class with only one method `show` for displaying
    3. `show` uses `show_title(o, ctx)`
    4. `ax` and `ctx` seem used interchangably in `show_title`
    """
    def show(o, ctx=None, **kwargs):
        show_title(o, ctx, **kwargs)
        return ctx
