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
###############################
from local.notebook.showdoc import _format_cls_doc, _format_enum_doc, _format_func_doc, is_enum, get_source_link, add_doc_links

###################
# return the nice representation of docs and source link to nbviewer
# elt = func/class
# `doc_string`
    # = determines if we show the docstring of the function or not.
# `name`
    # = can be used to provide an alternative to the name automatically found.
    # = but seems unatural to use
# title_level = 1,2,3,4 => how big is the title
# disp = True => nice markdown printing

def show_doc(elt, doc_string=True, name=None, title_level=None, disp=True, default_cls_level=2):
    "Show documentation for element `elt`. Supported types: class, function, and enum."
    elt = getattr(elt, '__func__', elt)
    name = name or qual_name(elt)
    if inspect.isclass(elt):
        if is_enum(elt.__class__):   name,args = _format_enum_doc(elt, name)
        else:                        name,args = _format_cls_doc (elt, name)
    elif isinstance(elt, Callable):  name,args = _format_func_doc(elt, name)
    else:                            name,args = f"<code>{name}</code>", ''
    link = get_source_link(elt)
    source_link = f'<a href="{link}" class="source_link" style="float:right">[source]</a>'
    title_level = title_level or (default_cls_level if inspect.isclass(elt) else 4)
    doc =  f'<h{title_level} id="{name}" class="doc_header">{name}{source_link}</h{title_level}>'
    doc += f'\n\n> {args}\n\n' if len(args) > 0 else '\n\n'
    if doc_string and inspect.getdoc(elt): doc += add_doc_links(inspect.getdoc(elt))
    if disp: display(Markdown(doc))
    else: return doc

def examples():

    show_doc(Pipeline)
    # %%
    #hide
    show_doc(Pipeline.composed)
    # %%
    #hide
    show_doc(ConfigKey)
    # %%
    #hide
    show_doc(compose)
    # %%
    #hide
    show_doc(untar_data)
    # %%
    #hide
    show_doc(add_docs)
    # %%
    #hide
    show_doc(Pipeline.__call__)
    # %%
    #hide
    from local.data.core import DataBunch
    show_doc(DataBunch.train_dl, name='DataBunch.train_dl')
    # %%
    # hide
    show_doc(Path.ls)
    
