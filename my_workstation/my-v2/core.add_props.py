from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

def add_props(f, n=2):
    """
    purpose:
    1. sometimes properties of a class are very similar in nature
    2. i.e., they follow the same structure but in different values
    3. to be specific, they are constructed by the same `f` but with different `i` values
    4. the `i` value difference can be described as `for i in range(n)`,
    5. where `n` refers to the number of properties, default to 2.
    """
    return (property(partial(f,i)) for i in range(n))


class _T(): a,b = add_props(lambda i,x:i*2)

t = _T()
test_eq(t.a,0)
test_eq(t.b,2)

class _T(): a,b,c,d = add_props(lambda i,x:i*2, n=4)
t = _T()
test_eq(t.a,0)
test_eq(t.b,2)
test_eq(t.c,4)
test_eq(t.d,6)

# more realistic usage examples
def more_realistic_examples():
    xt, yt = add_props(lambda i,x:x.tfms[i])
    train_dl, valid_dl = add_props(lambda i,x: x[i])
    train_ds, valid_ds = add_props(lambda i,x: x[i].dataset)
