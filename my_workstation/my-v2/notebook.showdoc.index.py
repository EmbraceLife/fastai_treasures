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


#hide
#Tricking jupyter notebook to have a __file__ attribute. All _file_ will be replaced by __file__
_file_ = Path('local').absolute()/'notebook'/'show_doc.py'

########################
# show the indexes with all the pytorch functions/classes

def _get_pytorch_index():
    if not (Path(_file_).parent/'index_pytorch.txt').exists(): return {}
    return json.load(open(Path(_file_).parent/'index_pytorch.txt', 'r'))

########################
# add pytorch function html address onto the indexes

def add_pytorch_index(func_name, url):
    "Add `func_name` in the PyTorch index for automatic links."
    index = _get_pytorch_index()
    if not url.startswith("https://pytorch.org/docs/stable/"):
        url = "https://pytorch.org/docs/stable/" + url
    index[func_name] = url
    json.dump(index, open(Path(_file_).parent/'index_pytorch.txt', 'w'), indent=2)

##########################
# index file and backup files

ind,ind_bak = Path(_file_).parent/'index_pytorch.txt',Path(_file_).parent/'index_pytorch.bak'

# wipe out the index
if ind.exists(): shutil.move(ind, ind_bak)
# doc(shutil.move)

##########################
# add functions/classes html address onto the indexes

assert _get_pytorch_index() == {}
add_pytorch_index('Tensor', 'tensors.html#torch-tensor')
assert _get_pytorch_index() == {'Tensor':'https://pytorch.org/docs/stable/tensors.html#torch-tensor'}
_get_pytorch_index()

###########################
# restore indexes from backup

if ind.exists(): shutil.move(ind_bak, ind)
_get_pytorch_index()
add_pytorch_index('Tensor', 'tensors.html#torch-tensor')
add_pytorch_index('device', 'tensor_attributes.html#torch-device')
add_pytorch_index('DataLoader', 'data.html#torch.utils.data.DataLoader')

_get_pytorch_index()
