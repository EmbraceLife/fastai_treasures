from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import * 

x = [1,1,0,5,0,3]
start = [9,10]
bidir = True
sort = True

##########################
# important! : not used for the following situation
x = ['dir/8/abc01.png', 'dir/4/abc02.png']
t1 = list(map(Path, x))
uniqueify(t1, sort=False, bidir=True)
OrderedDict.fromkeys(t1)
