from local.imports import *
from local.core import *
from local.data.pipeline import *
from multimethod import multimeta,DispatchError

# Empty pipeline is noop
class String():
    @staticmethod
    def show(o, ctx=None, **kwargs): return show_title(str(o), ctx=ctx)
class floatTfm(Transform):
    def encodes(self, x): return float(x)
    def decodes(self, x): return int(x)
float_tfm=floatTfm()
def neg(x) -> String: return -x
neg_tfm = Transform(neg, neg) 
# decodes is the same to encodes, as -x
pipe = Pipeline([neg_tfm, float_tfm]) # stack two tfms inside
t = pipe(2)
type(t)
pipe.decode(t)
pipe.show(t)
#show decodes up to the point of the first transform that introduced the type that shows, not included
test_stdout(lambda:pipe.show(t), '-2')