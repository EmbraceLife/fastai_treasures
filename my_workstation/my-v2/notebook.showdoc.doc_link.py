from local.imports import *
from local.notebook.core import *
from local.notebook.export import *
import inspect,enum,nbconvert
from IPython.display import Markdown,display
from IPython.core import page
from nbconvert import HTMLExporter

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

#########################
# additional imports for this function
from local.notebook.showdoc import is_fastai_module, _get_pytorch_index
FASTAI_DOCS = ''


#########################
# Create link to documentation for `name`, but still strings only 

def doc_link(name, include_bt:bool=True):
    "Create link to documentation for `name`."
    cname = f'`{name}`' if include_bt else name
    #Link to modules
    if is_fastai_module(name): return f'[{cname}]({FASTAI_DOCS}/{name}.html)'
    #Link to fastai functions
    try_fastai = source_nb(name, is_name=True)
    if try_fastai:
        page = '.'.join(try_fastai.split('_')[1:]).replace('.ipynb', '.html')
        return f'[{cname}]({FASTAI_DOCS}/{page}#{name})'
    #Link to PyTorch
    try_pytorch = _get_pytorch_index().get(name, None)
    if try_pytorch: return f'[{cname}]({try_pytorch})'
    #Leave as is
    return cname

def examples():
    assert doc_link('data.pipeline') == f'[`data.pipeline`]({FASTAI_DOCS}/data.pipeline.html)'
    assert doc_link('Pipeline') == f'[`Pipeline`]({FASTAI_DOCS}/data.pipeline.html#Pipeline)'
    assert doc_link('Transform.create') == f'[`Transform.create`]({FASTAI_DOCS}/data.pipeline.html#Transform.create)'
    assert doc_link('Tensor') == '[`Tensor`](https://pytorch.org/docs/stable/tensors.html#torch-tensor)'
    assert doc_link('Tenso') == '`Tenso`'
