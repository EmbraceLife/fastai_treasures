from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import patch


@patch
def ls(self:Path):
    """
    "Contents of path as a list"

    purpose:
    1. want to quickly add a method without going into cls Path
    2. use @patch decorator
    3. method job:
        a. iterate through content of this directory
        b. list them out
    """
    return list(self.iterdir())

path = Path();path
path = Path().cwd(); path
t = path.ls()
assert len(t)>0
t[:3]
# %%
#hide
pkl = pickle.dumps(path)# shrink size by half 
p2 =pickle.loads(pkl)
test_eq(path.ls()[0], p2.ls()[0])
sys.getsizeof(pkl)
sys.getsizeof(path)
sys.getsizeof(p2)
