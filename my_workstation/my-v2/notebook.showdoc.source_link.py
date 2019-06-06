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
######################
from local.notebook.showdoc import get_source_link

####################
# source_link(func, is_name=None, disp=True) = generate local nb link to func
# func = a string or object
# disp = True for link and False for string

def source_link(func, is_name=None, disp=True):
    "Show a relative link to the notebook where `func` is defined"
    is_name = is_name or isinstance(func, str)
    func_name = func if is_name else qual_name(func)
    link = get_source_link(func, local=True, is_name=is_name)
    if disp: display(Markdown(f'[{func_name}]({link})'))
    else: return link

# This function assumes you are in one notebook in the dev folder, otherwise
# you use `disp=False` to get the relative link. You can either pass an object
# or its name (by default `is_name` will look if `func` is a string or not, but
# you can override if there is some inconsistent behavior).

source_link(Pipeline)

assert source_link(chk, disp=False) == f'01_core.ipynb#Type-checking'
assert source_link('chk', disp=False) == f'01_core.ipynb#Type-checking'
