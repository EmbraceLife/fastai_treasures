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
from local.notebook.showdoc import doc_link, show_doc

######################
# add_doc_links(text) = add doc link to the text where a func/class appeared
# very convenient to add doc links when writing docs 

def add_doc_links(text):
    "Search for doc links for any item between backticks in `text`."
    pat = re.compile("\[`([^`]*)`\](?:\([^)]*\))|`([^`]*)`")
    def _replace_link(m): return doc_link(m.group(1) or m.group(2))
    return re.sub(pat, _replace_link, text)

# This function not only add links to backstick keywords, it also update the links that are already in the text.

tst = add_doc_links('This is an example of `Pipeline`')
assert tst == "This is an example of [`Pipeline`](/data.pipeline.html#Pipeline)"
tst = add_doc_links('Here we alread add a link in [`Tensor`](fake)')
assert tst == "Here we alread add a link in [`Tensor`](https://pytorch.org/docs/stable/tensors.html#torch-tensor)"

show_doc(Pipeline)
