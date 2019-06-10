from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

def chk(f):
    """
    purpose:
    1. In run time, how to make functions automatically check its input types?
    2. with a simple decorator @chk, life is much easier!
    """
    return typechecked(always=True)(f)

# a simple func to add this feature
@chk
def test_chk_int(a:int=1): pass

test_chk_int(1)
test_chk_int()
test_fail(lambda: test_chk_int('a'), contains='"a" must be int')

#####################
# a working but problematic example
@chk
def test_chk_str(a:str="1", b:float=1.0): pass

test_chk_str("2", 9.0)
test_chk_str("2", 9) # There should be a TypeError here, but !?
test_fail(lambda: test_chk_str("2", [9]), contains='"b" must be either float or int') # why it automatically accept int too?

#######################
# made_uncool
test_chk_int = chk(test_chk_int)
test_chk_int(1)
