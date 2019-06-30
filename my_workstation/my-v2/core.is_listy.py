from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L

assert is_listy([1])
assert is_listy(L([1]))
assert is_listy(slice(2)) # when and how to use slice?
assert not is_listy(torch.tensor([[1,3],[2,4]]))
