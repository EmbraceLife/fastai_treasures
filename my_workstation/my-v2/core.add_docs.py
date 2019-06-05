from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

def add_docs(cls, cls_doc=None, **docs):
    "Copy values from `docs` to `cls` docstrings, and confirm all public methods are documented"
    if cls_doc is not None: cls.__doc__ = cls_doc
    for k,v in docs.items():
        f = getattr(cls,k)
        if hasattr(f,'__func__'): f = f.__func__ # required for class methods
        f.__doc__ = v

    # List of public callables without docstring

    #####################
    # doc_improve: put n rather than c into the list for nice printing
    # nodoc = [n for n,c in vars(cls).items() if isinstance(c,Callable)
    #          and not n.startswith('_') and c.__doc__ is None]

    #####################
    # source_uncool: make source uncool to debug
    nodoc = []
    for n,c in vars(cls).items():
        if isinstance(c,Callable) and not n.startswith('_') and c.__doc__ is None:
            nodoc.append(n)

    assert not nodoc, f"Missing docs: {nodoc}"
    # doc_improve:
    # use cls.__name__ is nice to look at, official is just `cls`
    assert cls.__doc__ is not None, f"Missing class docs: {cls.__name__}"

class C():
    def func1():
        pass

    def func2():
        pass

######################
# provide a dict to `docs` and a string to `cls_doc` to add docs for Methods
# and class respectively
docs = {'func1':'what func1 is', 'func2':'what func2 is'}
cls_doc='nothing'
add_docs(C, cls_doc, **docs)
test_eq(C.__doc__, cls_doc)
C.func1.__doc__
C.func2.__doc__
# remove docs for two functions
C.func1.__doc__ = None
C.func2.__doc__ = None


###################
# set a value to None, to remove the doc
docs = {'func1':None, 'func2':'something'}
cls_doc='nothing'
# add_docs(C, cls_doc, **docs)
test_fail(lambda: add_docs(C, cls_doc, **docs), contains="Missing docs: ['func1']")
C.func1.__doc__
C.func2.__doc__

####################
# keep `docs={}` and `cls_doc=None` to see which has no docs yet
C.func1.__doc__ = 'soemthing'
C.func2.__doc__ = 'something else'
C.__doc__ = None
docs = {}
cls_doc=None
# add_docs(C, cls_doc, **docs)
test_fail(lambda: add_docs(C, cls_doc, **docs), contains="Missing class docs: C")
