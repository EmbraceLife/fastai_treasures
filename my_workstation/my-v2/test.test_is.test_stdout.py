from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import test_fail, test, equals, nequals, tensor, test_eq

def test_is(a,b):
    """
    "`test` that `a is b`"

    purpose:
    1. sometimes, we don't want equality but one step further for `is-ness`
    2. 'is-ness' or 'sameness' needs `operator.is`
    3. usually we have to do `test(a, b, operator.is, 'is')`
    4. we want to be lazy by typing `test_is(a,b)`
    5. we can use 4 to wrap 3
    """
    test(a,b,operator.is_, 'is')

test_fail(lambda: test_is([1], [1]))
a = [1] # here make sure `a` points to the same location in memory
test_is(a, a)
a1 = np.ndarray([1,2])
test_is(a1, a1)
a = tensor(1,2)
test_is(a, a)
test_fail(lambda: test_is(tensor(1,2), tensor(1,2)))

def test_stdout(f, exp, regex=False):
    """
    purpose:
    1. sometimes, we just want to double check on standard string output of func
    2. with help of `io.StringIO`, we can `redirect_stdout` of `f()` to `s`
    3. if `regex` is allowed, then `re.search` `exp` in `s.getvalue()`
        a. it should find the pattern/s there
        b. if not, raise Exception
    4. if `regex` not allowed, we `test_eq` on `s.getvalue()` and `f{exp}` or ''
    """
    s = io.StringIO()
    with redirect_stdout(s): f()
    if regex: assert re.search(exp, s.getvalue()) is not None
    else: test_eq(s.getvalue(), f'{exp}\n' if len(exp) > 0 else '')

test_stdout(lambda: print('hi'), 'hi')

test_fail(lambda: test_stdout(lambda: print('hi'), 'ho'))

test_stdout(lambda: 1+1, '')

test_stdout(lambda: print('hi there!'), r'^hi.*!$', regex=True)
