# Fastai-v2 Docs on Each Item

- search "doc_improve:" with vim Ag to see my proposed source improvements in the source files below
- search "source_uncool:" with vim Ag to see how clean and compact official source code is and how to make it uncool for debugging
- search "not_finished": for official source but unfinished properly

[core.newchk](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.newchk.py)
> enable Class_T(t) return the same instance, rather than creating new instance, if t is an instance of the Class_T

[core.patch](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.patch.py)
> enable a function to add itself to the Class of its first parameter

[core.chk](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.chk.py)
> enable a function to check on its parameters types

[core.ls](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.ls.py)
> enable a Path object with a new method to check its contents on the immediate level

[core.tensor](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.tensor.py)
> put array-like, list, tuple, or just a few numbers into an tensor

[core.tensor.ndim](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.tensor.ndim.py)
> add `ndim` as a property to any tensor object to return num of dimensions

[core.add_docs](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.add_docs.py)
> to add docs for Class and methods and report which has no docs yet

[core.docs](https://github.com/EmbraceLife/my-v2/blob/master/dev/core.docs.py)
> to enable a Class to set up its docs (unfinished by official source yet)
