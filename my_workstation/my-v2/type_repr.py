from local.imports import *
from local.notebook.core import *
from local.notebook.export import *
import inspect,enum,nbconvert
from IPython.display import Markdown,display
from IPython.core import page
from nbconvert import HTMLExporter
# %% markdown
# # Show doc
# > Functions to show the doc cells in notebooks
# %%
from local.core import compose, add_docs, chk
from local.data.pipeline import Pipeline
from local.data.external import untar_data, ConfigKey

test_cases = [
    Pipeline,   #Basic class
    ConfigKey,  #Enum
    compose,    #Func with star args and type annotation
    untar_data, #Func with defaults
    add_docs,   #Func with kwargs
    Path.ls     #Monkey-patched
]
###################
from local.notebook.showdoc import doc_link


def type_repr(t):
    "Representation of type `t` (in a type annotation)"
    if getattr(t, '__args__', None):
        args = t.__args__
        if len(args)==2 and args[1] == type(None):
            return f'`Optional`\[{type_repr(args[0])}\]'
        reprs = ', '.join([type_repr(o) for o in args])
        return f'{doc_link(get_name(t))}\[{reprs}\]'
    else: return doc_link(get_name(t))


######################
# type_repr(t) = represent type while add links to it 

tst = type_repr(Optional[Tensor])
assert tst == '`Optional`\\[[`Tensor`](https://pytorch.org/docs/stable/tensors.html#torch-tensor)\\]'
tst = type_repr(Union[Tensor, float])
assert tst == '`Union`\\[[`Tensor`](https://pytorch.org/docs/stable/tensors.html#torch-tensor), `float`\\]'
