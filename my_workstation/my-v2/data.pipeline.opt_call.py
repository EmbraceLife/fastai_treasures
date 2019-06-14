from dev.local.imports import *
from dev.local.test import *
from dev.local.core import *
from dev.local.notebook.showdoc import show_doc

def opt_call(f, fname='__call__', *args, **kwargs):
    """
    oneliner:
    1. "Call `f.{fname}(*args, **kwargs)`, or `noop` if not defined"

    purpose:
    1. sometimes we want the freedom to call any methods of a func or object
        - without worrying whether the method is available or not
        - more importantly, very convenient if in need to run many in a loop!!!
            - shift+cmd+F `opt_call` to see other use cases
        - if not available, why not just run `noop` instead
    2. to achieve it, we won't do `object.method(*args, **kwargs)` of course
    3. we create a new func `opt_call` to
        - make func/object, methods, and inputs as insertable arguments
    3. this way, we can
        3.1 try any object/func
        3.2 try any method name
        3.3 do anything when the method is not available,
            - such as pass on a `noop()` to make it end smoothly.
    """
    return getattr(f,fname,noop)(*args, **kwargs)

# pdb
opt_call(operator.neg, '__call__', 2)
opt_call(list, 'foobar', [2])
a=[2,1]
opt_call(list, 'sort', a)
