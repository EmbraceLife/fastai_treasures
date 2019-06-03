from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

# ### Type checking
# Runtime type checking is handy, so let's make it easy!

def chk(f): return typechecked(always=True)(f)

# Decorator for a function to check that type-annotated arguments receive arguments of the right type.
def test_chk_int(a:int=1): pass
test_chk_int = chk(test_chk_int)
test_chk_int(1)

@chk
def test_chk_int(a:int=1): pass

test_chk_int(1)
test_chk_int()

test_fail(lambda: test_chk_int('a'), contains='"a" must be int')


@chk
def test_chk_str(a:str="1", b:float=1.0): pass

test_chk_str("2", 9.0)
test_chk_str("2", 9) # There should be a TypeError here, but !?
test_chk_str("2", [9]) # TypeError expected, good.

test_fail(lambda: test_chk_str("2", [9]), contains='"b" must be either float or int') # why it automatically accept int too?
