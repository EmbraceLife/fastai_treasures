from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test, equals, nequals, tensor


#########################


def is_close(a,b,eps=1e-5):
    """
    Is `a` within `eps` of `b`
    purpose:
    1. sometimes, you don't want equality but closeness.
    2. you want to see whether two values or list... to be close enough
    3. we can separate them into three cases:
    4. `a, b` are `Tensor or ndarray`, return `(abs(a-b)<eps).all()`
    5. `a, b` are `Iterator or Generator`,
        a. make them `np.array`
        b. and then do `is_close`
    6. `a, b` are just scalar probably, then return `abs(a-b)<eps`
    7. `eps`, set the epsilon (how close you want) by you
    """
    if isinstance(a, (Tensor,np.ndarray)) or isinstance(b, (Tensor,np.ndarray)):
        return (abs(a-b)<eps).all()
    if isinstance(a, (Iterable,Generator)) or isinstance(b, (Iterable,Generator)):
        return is_close(np.array(a), np.array(b), eps=eps)
    return abs(a-b)<eps

def test_close(a,b,eps=1e-5):
    """
    "`test` that `a` is within `eps` of `b`"
    purpose:
    1. We want unified names like `test_close`
    2. We often do `test(a, b, partial(is_close, eps=...), "close")`
    3. we want to be lazy by just typing `test_close(a, b, eps=...)`
    4. so we use 3 to wrap 2
    """
    test(a,b,partial(is_close,eps=eps),'close')

test_close(1,1.001,eps=1e-2)
test_fail(lambda: test_close(1,1.001))
test_close([-0.001,1.001], [0.,1.], eps=1e-2)
test_close(np.array([-0.001,1.001]), np.array([0.,1.]), eps=1e-2)
test_close(torch.tensor([-0.001,1.001]), torch.tensor([0.,1.]), eps=1e-2)
