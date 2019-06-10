from local.imports import *
from local.notebook.showdoc import show_doc

#################

def test_fail(f, msg='', contains=''):
    """
    "Fails with `msg` unless `f()` raises an exception and (optionally) has `contains` in `e.args`"

    purpose:
    - sometimes things do fail, and we want to anticipate the failures

    steps:
    - 1. we `try` on the target function `f()`
    - 2. expectedly, we will catch `Exception` by asserting on
            having an empty string in `contains`
    - 3. or we will catch exception by asserting on having a string `contains`
            which is part of `Exception` message `e`
    - 4. well, if unexpectedly no Exception rise, we will `assert False`
            to send an error message in `msg`
    """
    try:
        f()
        assert False,f"Expected exception but none raised. {msg}"
    except Exception as e: assert not contains or contains in str(e)


#################
# define two funcs to raise exceptions

def examples():
    def _fail(): raise Exception("foobar")
    test_fail(_fail, contains="foo")

    def _fail(): raise Exception()
    test_fail(_fail)
