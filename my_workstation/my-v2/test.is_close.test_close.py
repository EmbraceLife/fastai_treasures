from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test, equals, nequals, tensor


#########################
# is_close = is `a` close enough to `b` within `eps`
# is_close = is also iterative so can work on iterable and generator a, b
# a, b = Tensor, array, Iterable, Generator, or single values

def is_close(a,b,eps=1e-5):
    "Is `a` within `eps` of `b`"
    # to work in tensor or array
    if isinstance(a, (Tensor,np.ndarray)) or isinstance(b, (Tensor,np.ndarray)):
        return (abs(a-b)<eps).all()

    # to work on iterable or generator
    if isinstance(a, (Iterable,Generator)) or isinstance(b, (Iterable,Generator)):
        return is_close(np.array(a), np.array(b), eps=eps)

    # to work on single values
    return abs(a-b)<eps

#######################
# test_close = to test is_close with a, b and eps
# partial = to tailor a specific eps with is_close
# output = nothing if true
# output = exception with cname, a, b if false

def test_close(a,b,eps=1e-5):
    "`test` that `a` is within `eps` of `b`"
    test(a,b,partial(is_close,eps=eps),'close')

def examples():

    test_close(1,1.001,eps=1e-2)
    test_fail(lambda: test_close(1,1.001))
    test_close([-0.001,1.001], [0.,1.], eps=1e-2)
    test_close(np.array([-0.001,1.001]), np.array([0.,1.]), eps=1e-2)
    test_close(torch.tensor([-0.001,1.001]), torch.tensor([0.,1.]), eps=1e-2)

def inspectors():

    sig(all)
    is_close(np.array([-0.001,1.001]), np.array([0.,1.]), eps=1e-2)
