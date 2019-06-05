from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

#########################
# we often need to use the following code
if a is None:
    return b
else:
    return a

##########################
# therefore it worths of refactoring it into
def ifnone(a, b):
    "`b` if `a` is None else `a`"
    return b if a is None else a

test_eq(ifnone(None,1), 1)
test_eq(ifnone(2   ,1), 2)

# However, be careful, because python will evaluate *both* `a` and `b` when
# calling `ifnone` (which it doesn't do if using the `if` version directly).
test_fail(lambda: ifnone(1,1/0), contains='division by zero')
