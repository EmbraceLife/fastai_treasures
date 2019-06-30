from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
from local.data.pipeline import *

Func('sqrt')(math)
Func('sqrt')(torch)
@patch
def powx(x:math, a): return math.pow(x,a)
@patch
def powx(x:torch, a): return torch.pow(x,a)
tst = Func('powx',a=2)([math, torch])

Func('pow', a=3)([math, torch])
test_eq([f.func for f in tst], [math.powx, torch.powx])
for t in tst: test_eq(t.keywords, {'a': 2})