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

_file_ = Path('local').absolute()/'notebook'/'show_doc.py'

def is_fastai_module(name):
    "Test if `name` is a fastai module."
    dir_name = os.path.sep.join(name.split('.'))
    return (Path(_file_).parent.parent/f"{dir_name}.py").exists()

assert is_fastai_module('data.external')
assert is_fastai_module('core')
assert not is_fastai_module('export')
