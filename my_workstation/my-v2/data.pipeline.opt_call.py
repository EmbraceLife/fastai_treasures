from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc
#################

# `opt_call(f, fname='__call__', *args, **kwargs)`
# = call `f.{fname}(*args, **kwargs)` or call `noop()`,
# = if `f.{fname}` is not defined

def opt_call(f, fname='__call__', *args, **kwargs):
    "Call `f.{fname}(*args, **kwargs)`, or `noop` if not defined"
    return getattr(f,fname,noop)(*args, **kwargs)

# pdb
opt_call(operator.neg, '__call__', 2)
opt_call(list, 'foobar', [2])

# nb
test_eq(opt_call(operator.neg, '__call__', 2), -2)
test_eq(opt_call(list, 'foobar', [2]), [2])

a=[2,1]
opt_call(list, 'sort', a)
test_eq(a, [1,2])
