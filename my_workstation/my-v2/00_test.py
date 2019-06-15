# %%
#default_exp test
# %%
#export
from local.imports import *
from local.notebook.showdoc import show_doc
# %% markdown
# # Test
#
# > Helper functions to quickly write tests in notebooks
# %% markdown
# ## Simple test functions
# %% markdown
# We can test for equality (`test_eq`) or inequality (`test_ne`) of arrays, tensors, and scalars, and lists of any of these. We can also check that code raises an exception when that's expected (`test_fail`).
# %%
#export
def test_fail(f, msg='', contains=''):
    "Fails with `msg` unless `f()` raises an exception and (optionally) has `contains` in `e.args`"
    try:
        f()
        assert False,f"Expected exception but none raised. {msg}"
    except Exception as e: assert not contains or contains in str(e)
# %%
def _fail(): raise Exception("foobar")
test_fail(_fail, contains="foo")

def _fail(): raise Exception()
test_fail(_fail)
# %%
#export
def test(a, b, cmp,cname=None):
    "`assert` that `cmp(a,b)`; display inputs and `cname or cmp.__name__` if it fails"
    if cname is None: cname=cmp.__name__
    assert cmp(a,b),f"{cname}:\n{a}\n{b}"
# %%
test([1,2],[1,2], operator.eq)
test_fail(lambda: test([1,2],[1], operator.eq))
test([1,2],[1],   operator.ne)
test_fail(lambda: test([1,2],[1,2], operator.ne))
# %%
show_doc(all_equal)
# %%
test(['abc'], ['abc'],  all_equal)
# %%
show_doc(equals)
# %%
test([['abc'],['a']], [['abc'],['a']],  equals)
# %%
#export
def nequals(a,b):
    "Compares `a` and `b` for `not equals`"
    return not equals(a,b)
# %%
test(['abc'], ['ab' ], nequals)
# %% markdown
# ## test_eq test_ne, etc...
# %% markdown
# Just use `test_eq`/`test_ne` to test for `==`/`!=`. We define them using `test`:
# %%
#exports
def test_eq(a,b):
    "`test` that `a==b`"
    test(a,b,equals, '==')
# %%
test_eq([1,2],[1,2])
test_eq([1,2],map(int,[1,2]))
test_eq(torch.tensor(1),1)
test_eq(1,torch.tensor(1))
test_eq(torch.tensor([1,2]),torch.tensor([1,2]))
test_eq(array([1,2]),array([1,2]))
test_eq([array([1,2]),3],[array([1,2]),3])
# %%
#exports
def test_ne(a,b):
    "`test` that `a!=b`"
    test(a,b,nequals,'!=')
# %%
test_ne([1,2],[1])
test_ne([1,2],[1,3])
test_ne(torch.tensor([1,2]),torch.tensor([1,1]))
test_ne(array([1,2]),array([1,1]))
test_ne([array([1,2]),3],[array([1,2])])
test_ne([3,4],torch.tensor([3]))
test_ne([3,4],torch.tensor([3,5]))
# %%
#exports
def is_close(a,b,eps=1e-5):
    "Is `a` within `eps` of `b`"
    if isinstance(a, (Tensor,np.ndarray)) or isinstance(b, (Tensor,np.ndarray)):
        return (abs(a-b)<eps).all()
    if isinstance(a, (Iterable,Generator)) or isinstance(b, (Iterable,Generator)):
        return is_close(np.array(a), np.array(b), eps=eps)
    return abs(a-b)<eps
# %%
#exports
def test_close(a,b,eps=1e-5):
    "`test` that `a` is within `eps` of `b`"
    test(a,b,partial(is_close,eps=eps),'close')
# %%
test_close(1,1.001,eps=1e-2)
test_fail(lambda: test_close(1,1.001))
test_close([-0.001,1.001], [0.,1.], eps=1e-2)
test_close(np.array([-0.001,1.001]), np.array([0.,1.]), eps=1e-2)
test_close(torch.tensor([-0.001,1.001]), torch.tensor([0.,1.]), eps=1e-2)
# %%
#exports
def test_is(a,b):
    "`test` that `a is b`"
    test(a,b,operator.is_, 'is')
# %%
test_fail(lambda: test_is([1], [1]))
a = [1]
test_is(a, a)
# %%
#export
def test_stdout(f, exp, regex=False):
    s = io.StringIO()
    with redirect_stdout(s): f()
    if regex: assert re.search(exp, s.getvalue()) is not None
    else: test_eq(s.getvalue(), f'{exp}\n' if len(exp) > 0 else '')
# %%
test_stdout(lambda: print('hi'), 'hi')
test_fail(lambda: test_stdout(lambda: print('hi'), 'ho'))
test_stdout(lambda: 1+1, '')
test_stdout(lambda: print('hi there!'), r'^hi.*!$', regex=True)
# %% markdown
# ## Export -
# %%
#hide
from local.notebook.export import notebook2script
notebook2script(all_fs=True)
# %%
