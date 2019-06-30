from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import *

match = [1,1]
item = [1,2]
test_eq(replicate([1,2], t),([1,2],[1,2]))
test_eq(replicate(1, t),(1,1))
test_eq(replicate((1,2), t),((1, 2), (1, 2)))

