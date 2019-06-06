from local.imports import *
from local.notebook.showdoc import show_doc

#################
# anticipate the error or exception
# f = the function to be run
# msg = message when no error or exception, default ""
# contains = part of message from Exception, default ""

def test_fail(f, msg='', contains=''):
    "Fails with `msg` unless `f()` raises an exception and (optionally) has `contains` in `e.args`"
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
