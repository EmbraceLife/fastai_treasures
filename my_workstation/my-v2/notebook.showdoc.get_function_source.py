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
#################################

#export
SOURCE_URL = "https://github.com/fastai/fastai_docs/tree/master/dev/"


############################
# get_function_source(func) = return the link to the func source online

def get_function_source(func):
    "Return link to `func` in source code"
    try: line = inspect.getsourcelines(func)[1]
    except Exception: return ''
    module = inspect.getmodule(func).__name__.replace('.', '/') + '.py'
    return f"{SOURCE_URL}{module}#L{line}"

def examples():

    get_function_source(Pipeline)
# More important than source code, we want to quickly jump to where the function is defined in a dev notebook.
