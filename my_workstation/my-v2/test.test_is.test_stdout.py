from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test, equals, nequals, tensor, test_eq





#########################
# test_is = test whether `a` is exactly `b`
# output = nothing if true
# output = exception with cname `is`, a, b if false
def test_is(a,b):
    "`test` that `a is b`"
    test(a,b,operator.is_, 'is')

def examples():
    # strange_behavior
    test_fail(lambda: test_is([1], [1]))
    a = [1]
    test_is(a, a)
    a1 = np.ndarray([1,2])
    test_is(a1, a1)
    a = tensor(1,2)
    test_is(a, a)
    # this is strange_behavior !!
    test_fail(lambda: test_is(tensor(1,2), tensor(1,2)))

#######################
# test_stdout = to test whether f() has expected output
# output = nothing if true
# output = exception with cname, a, b if false
def test_stdout(f, exp, regex=False):
    s = io.StringIO()
    with redirect_stdout(s): f()
    if regex: assert re.search(exp, s.getvalue()) is not None
    else: test_eq(s.getvalue(), f'{exp}\n' if len(exp) > 0 else '')

def examples():
    test_stdout(lambda: print('hi'), 'hi')

    test_fail(lambda: test_stdout(lambda: print('hi'), 'ho'))

    test_stdout(lambda: 1+1, '')

    test_stdout(lambda: print('hi there!'), r'^hi.*!$', regex=True)
