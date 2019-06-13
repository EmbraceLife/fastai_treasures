from local.imports import *
from local.test import *
from local.notebook.showdoc import show_doc


def bunzip(fn):
    """
    purpose:
    1. to unzip bz2 files
    2. don't unzip if it is already done, and make an exception message
    3. see the example on how to unzip and delete files at ease
    """
    fn = Path(fn)
    assert fn.exists(), f"{fn} doesn't exist"
    out_fn = fn.with_suffix('')
    assert not out_fn.exists(), f"{out_fn} already exists"
    with bz2.BZ2File(fn, 'rb') as src, out_fn.open('wb') as dst:
        for d in iter(lambda: src.read(1024*1024), b''): dst.write(d)

f = Path('files/test.txt')
if f.exists(): f.unlink()
bunzip('files/test.txt.bz2')
t = f.open().readlines(); t
f.unlink()
show_doc(f.unlink)
