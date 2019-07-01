from local.imports import *
from local.core import *
from local.data.pipeline import *
from multimethod import multimeta,DispatchError

tfm = Transform(operator.neg, decodes=operator.neg)
start = 4
t = tfm(start)
test_eq(t, -4)
test_eq(t, tfm[start]) #You can use a transform as a dataset
test_eq(tfm.decode(t), start)