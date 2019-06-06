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

###################
# is_enum = whether the cls is enum.Enum or enum.EnumMeta
def is_enum(cls):
    "Check if `cls` is an enum or another type of class"
    return cls.__class__ == enum.Enum or cls.__class__ == enum.EnumMeta

def examples():
    assert is_enum(ConfigKey)
    assert not is_enum(Pipeline)
