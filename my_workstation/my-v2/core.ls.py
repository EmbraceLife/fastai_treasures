from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

def patch(f):
    "Decorator: add `f` to the first parameter's class (based on f's type annotations)"
    cls = next(iter(f.__annotations__.values()))
    nf = copy.copy(f)
    functools.update_wrapper(nf,f)
    nf.__qualname__ = f"{cls.__name__}.{f.__name__}"
    setattr(cls, f.__name__, nf)
    return f

@patch
def ls(self:Path):
    "Contents of path as a list"
    return list(self.iterdir())
# %% markdown
# We add an `ls()` method to `pathlib.Path` which is simply defined as
# `list(Path.iterdir())`, mainly for convenience in REPL environments
# such as notebooks.
# %%
path = Path()
t = path.ls()
assert len(t)>0
t[0]
# %%
#hide
pkl = pickle.dumps(path)
p2 =pickle.loads(pkl)
test_eq(path.ls()[0], p2.ls()[0])
