from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

L([[1,2],[3,4]])
L([[1,2],[3,4]]).tensored()
L([[1,2],[3,4]]).stack(dim=0)
L([[1,2],[3,4]]).stack(dim=1)
L([[1,2],[3,4]]).cat(dim=0)
L([[1,2],[3,4]]).cat(dim=-1)


