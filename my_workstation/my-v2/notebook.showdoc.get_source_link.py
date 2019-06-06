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
#####################


FASTAI_NB_DEV = 'https://nbviewer.jupyter.org/github/fastai/fastai_docs/blob/master/dev/'

########################
# get_source_link(func, local=False, is_name=None) =
# 1. return the link to notebook at specific section for the `func`
# 2. `func` can be a string or object
# 3. local = True, gives your local link to the notebook 

def get_source_link(func, local=False, is_name=None):
    "Return a link to the notebook where `func` is defined."
    pref = '' if local else FASTAI_NB_DEV
    is_name = is_name or isinstance(func, str)
    src = source_nb(func, is_name=is_name, return_all=True)
    if src is None: return '' if is_name else get_function_source(func)
    find_name,nb_name = src
    nb = read_nb(nb_name)
    pat = re.compile(f'^{find_name}\s+=|^(def|class)\s+{find_name}\s*\(', re.MULTILINE)
    if len(find_name.split('.')) == 2:
        clas,func = find_name.split('.')
        pat2 = re.compile(f'@patch\s*\ndef\s+{func}\s*\([^:]*:\s*{clas}\s*(?:,|\))')
    else: pat2 = None
    for i,cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            if re.search(pat, cell['source']):  break
            if pat2 is not None and re.search(pat2, cell['source']): break
    if re.search(pat, cell['source']) is None and (pat2 is not None and re.search(pat2, cell['source']) is None):
        return '' if is_name else get_function_source(func)
    header_pat = re.compile(r'^\s*#+\s*(.*)$')
    while i >= 0:
        cell = nb['cells'][i]
        if cell['cell_type'] == 'markdown' and re.search(header_pat, cell['source']):
            title = re.search(header_pat, cell['source']).groups()[0]
            anchor = '-'.join([s for s in title.split(' ') if len(s) > 0])
            return f'{pref}{nb_name}#{anchor}'
        i -= 1
    return f'{pref}{nb_name}'

def examples():

    assert get_source_link(Pipeline.composed) == get_source_link(Pipeline)
    assert get_source_link('Pipeline') == get_source_link(Pipeline)
    assert get_source_link(chk) == f'{FASTAI_NB_DEV}01_core.ipynb#Type-checking'
    assert get_source_link(chk, local=True) == f'01_core.ipynb#Type-checking'
    assert get_source_link('Path.ls') == f'{FASTAI_NB_DEV}01_core.ipynb#`Path.ls`'

# You can either pass an object or its name (by default `is_name` will look if
# `func` is a string or not, but you can override if there is some inconsistent
# behavior). `local` will return a local link.
