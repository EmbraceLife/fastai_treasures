from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L

def custom_dir(c, add:List):
    """
    Why need `custom_dir`
    - sometimes want to see both `dir(c)` and `dict(c)`
    - why don't we put them together and get them in one go?
    - what if we want to see additional methods?
        - we put the additional/extra methods into a list `add`
    - in one go, we output the names in `dir, dict, add`
    """
    return dir(type(c)) + list(c.__dict__.keys()) + add

show_doc(custom_dir)
custom_dir(int, list())[-2:]
