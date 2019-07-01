from local.imports import *
from local.core import *
from local.data.pipeline import *
from multimethod import multimeta,DispatchError

def dummy_tfm(x:float, y:float): return x**y
tfm = Transform([dummy_tfm, operator.neg])
tfm(((2,3),4)) # __call__, _apply(..t,filt)

