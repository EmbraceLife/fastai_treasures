from local.imports import *
from local.core import *
from local.data.pipeline import *
from multimethod import multimeta,DispatchError

class _FiltAddOne(Transform):
    filt=1
    def encodes(self, x): return x+1
    def decodes(self, x): return x-1
class String():
    @staticmethod
    def show(o, ctx=None, **kwargs): return show_title(str(o), ctx=ctx)
class floatTfm(Transform):
    def encodes(self, x): return float(x)
    def decodes(self, x): return int(x)
float_tfm=floatTfm()
def neg(x) -> String: return -x
neg_tfm = Transform(neg, neg) 
#Check filtering is properly applied
pipe = Pipeline([neg_tfm, float_tfm, _FiltAddOne()])
pipe.setup(items=[2])
pipe.tfms