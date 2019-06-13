from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import L, tensor
def mapper(f):
    """
    purpose:
    1. outside L, it would be nice to have sth similar to `L.mapped`
    2. it would be nice if we can do `mapper(f)(data)`
        2.1 `f` is the func we want to apply to every item of 'data'
        2.2 `data` is the data including many items
    3. `mapper(f)` return a lambda func, inside the func, it can
        3.1 loop through every item `o_` from `o` (or `data`)
        3.2 apply `f` on each `o_`
        3.3 put each output into a single list
    4. the lambda func returned from `mapper(f)` will take `(data)` to run
    So, this above is the logic of `mapper(f)(data)`
    """
    return lambda o: [f(o_) for o_ in o]

mapper(lambda o:o*2)(range(3))
mapper(lambda o:o*2)(L(1,2,3))
mapper(lambda o:o*2)(array([1,2,3]))
mapper(lambda o:o*2)(tensor([1,2,3]))
