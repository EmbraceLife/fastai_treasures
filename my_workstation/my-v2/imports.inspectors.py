# my own inspection helpers
from inspect import getdoc as doc, getsourcelines as source, getmodule as module, signature as sig, getmembers as member, getmro as clstree

def clsstree(a):
    return getmro(a.__class__)

def dr(a):
    return a.__dir__()

def dt(a):
    return a.__dict__

doc(DataLoader)
sig(DataLoader)
source(DataLoader)
module(DataLoader)
member(DataLoader)
