from local.imports import *
from local.core import *
from local.data.pipeline import *
from multimethod import multimeta,DispatchError

#Using supertype encodes/decodes, we have a hacky way, might want to simplify it.
class _AddOne(Transform):
    def encodes(self, x:numbers.Integral): return x+1
    def encodes(self, x:int): return self._get_func(self.encodes, numbers.Integral)(x)*2
    def decodes(self, x:numbers.Integral): return x-1
    def decodes(self, x:int): return self._get_func(self.decodes, numbers.Integral)(x/2)
    
tfm = _AddOne()
start = 2
tfm.accept_types(numbers.Integral)
tfm.return_type()
t = tfm(start)
tfm.decode(t)
tfm.accept_types(int)
tfm.return_type()
t = tfm(start)
tfm.decode(t) # why this returns a float
