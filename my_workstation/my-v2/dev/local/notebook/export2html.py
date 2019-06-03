#AUTOGENERATED! DO NOT EDIT! File to edit: dev/93_notebook_export2html.ipynb (unless otherwise specified).

__all__ = ['remove_widget_state', 'hide_cells', 'clean_exports', 'treat_backticks', 'convert_links', 'add_jekyll_notes',
           'copy_images', 'remove_hidden', 'find_default_level', 'add_show_docs', 'remove_fake_headers', 'remove_empty',
           'get_metadata', 'ExecuteShowDocPreprocessor', 'execute_nb', 'process_cells', 'process_cell', 'convert_nb',
           'convert_all']

from ..imports import *
from ..core import compose
from .export import *
from .showdoc import *
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
from nbconvert import HTMLExporter
from nbformat.sign import NotebookNotary
from traitlets.config import Config

def remove_widget_state(cell):
    "Remove widgets in the output of `cells`"
    if cell['cell_type'] == 'code' and 'outputs' in cell:
        cell['outputs'] = [l for l in cell['outputs']
                           if not ('data' in l and 'application/vnd.jupyter.widget-view+json' in l.data)]
    return cell

def hide_cells(cell):
    "Hide `cell` that need to be hidden"
    if check_re(cell, r's*show_doc\(|^\s*#\s*(export)\s+'):
        cell['metadata'] = {'hide_input': True}
    return cell

def clean_exports(cell):
    "Remove exports flag from `cell`"
    cell['source'] = re.sub(r'^#\s*exports[^\n]*\n', '', cell['source'])
    return cell

def treat_backticks(cell):
    "Add links to backticks words in `cell`"
    if cell['cell_type'] == 'markdown': cell['source'] = add_doc_links(cell['source'])
    return cell

def convert_links(cell):
    "Convert the .ipynb links to .html"
    if cell['cell_type'] == 'markdown':
        cell['source'] = re.sub(r'\[([^http][^\]]*)\]\(([^\)]*).ipynb\)', r'[\1](\2.html)', cell['source'])
    return cell

def add_jekyll_notes(cell):
    "Convert block quotes to jekyll notes in `cell`"
    t2style = {'Note': 'info', 'Warning': 'danger', 'Important': 'warning'}
    def _inner(m):
        title,text = m.groups()
        style = t2style.get(title, None)
        if style is None: return f"> {m.groups()[0]}: m.groups()[1]"
        res = f'<div markdown="span" class="alert alert-{style}" role="alert">'
        return res + f'<i class="fa fa-{style}-circle"></i> <b>{title}: </b>{text}</div>'
    if cell['cell_type'] == 'markdown':
        cell['source'] = re.sub(r'>\s*([^:]*):\s*([^\n]*)(?:\n|$)', _inner, cell['source'])
    return cell

def copy_images(cell, fname, dest):
    pat = re.compile(r'^!\[[^\]]*\]\(([^\)]*)\)|<img src="([^"]*)"', re.MULTILINE)
    if cell['cell_type'] == 'markdown' and re.search(pat, cell['source']):
        grps = re.search(pat, cell['source']).groups()
        src = grps[0] or grps[1]
        os.makedirs((Path(dest)/src).parent, exist_ok=True)
        shutil.copy(Path(fname).parent/src, Path(dest)/src)
    return cell

def remove_hidden(cells):
    "Remove in `cells` the ones with a flag `#hide` or `#default_exp`"
    res = []
    pat = re.compile(r'^\s*#\s*(hide|default_exp)\s+')
    for cell in cells:
        if cell['cell_type']=='markdown' or re.search(pat, cell['source']) is None:
            res.append(cell)
    return res

def find_default_level(cells):
    "Find in `cells` the default export module."
    for cell in cells:
        tst = check_re(cell, r'^\s*#\s*default_cls_lvl\s*(\d*)\s*$')
        if tst: return int(tst.groups()[0])
    return 2

def _show_doc_cell(name, cls_lvl=None):
    return {'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': f"show_doc({name}{'' if cls_lvl is None else f', default_cls_level={cls_lvl}'})"}

def add_show_docs(cells, cls_lvl=None):
    "Add `show_doc` for each exported function or class"
    sd_pat = re.compile(r'^show_doc\s*\(\s*([^,\)\s]*)[,\)\s]', re.MULTILINE)
    documented = [re.search(sd_pat, cell['source']).groups()[0] for cell in cells
                  if cell['cell_type']=='code' and re.search(sd_pat, cell['source']) is not None]
    res = []
    for cell in cells:
        res.append(cell)
        if check_re(cell, r'^\s*#\s*exports?\s*'):
            names = export_names(cell['source'], func_only=True)
            for n in names:
                if n not in documented: res.append(_show_doc_cell(n, cls_lvl=cls_lvl))
    return res

def remove_fake_headers(cells):
    "Remove in `cells` the fake header"
    res = []
    pat = re.compile(r'#+.*-$')
    for cell in cells:
        if cell['cell_type']=='code' or re.search(pat, cell['source']) is None:
            res.append(cell)
    return res

def remove_empty(cells):
    "Remove in `cells` the empty cells"
    return [c for c in cells if len(c['source']) >0]

def get_metadata(cells):
    "Find the cell with title and summary in `cells`."
    pat = re.compile('^\s*#\s*([^\n]*)\n*>\s*([^\n]*)')
    for i,cell in enumerate(cells):
        if cell['cell_type'] == 'markdown':
            match = re.match(pat, cell['source'])
            if match:
                cells.pop(i)
                return {'keywords': 'fastai',
                        'summary' : match.groups()[1],
                        'title'   : match.groups()[0]}
    return {'keywords': 'fastai',
            'summary' : 'summary',
            'title'   : 'Title'}

class ExecuteShowDocPreprocessor(ExecutePreprocessor):
    "An `ExecutePreprocessor` that only executes `show_doc` and `import` cells"
    def preprocess_cell(self, cell, resources, index):
        pat = re.compile(r"^\s*show_doc\(([^\)]*)\)|^\s*#\s*exports?\s*", re.MULTILINE)
        if 'source' in cell and cell['cell_type'] == "code":
            if re.search(pat, cell['source']):
                return super().preprocess_cell(cell, resources, index)
        return cell, resources

def _import_show_doc_cell(name=None):
    "Add an import show_doc cell + deal with the __file__ hack if necessary."
    source = f"#export\nfrom local.notebook.showdoc import show_doc"
    if name: source += f"\nfrom pathlib import Path\n__file__ = {name}"
    return {'cell_type': 'code',
            'execution_count': None,
            'metadata': {'hide_input': True},
            'outputs': [],
            'source': source}

def execute_nb(nb, metadata=None, show_doc_only=True, name=None):
    "Execute `nb` (or only the `show_doc` cells) with `metadata`"
    nb['cells'].insert(0, _import_show_doc_cell(name))
    ep_cls = ExecuteShowDocPreprocessor if show_doc_only else ExecutePreprocessor
    ep = ep_cls(timeout=600, kernel_name='python3')
    metadata = metadata or {}
    pnb = nbformat.from_dict(nb)
    ep.preprocess(pnb, metadata)
    return pnb

def _exporter():
    exporter = HTMLExporter(Config())
    exporter.exclude_input_prompt=True
    exporter.exclude_output_prompt=True
    exporter.template_file = 'jekyll.tpl'
    exporter.template_path.append(str(Path(__file__).parent))
    return exporter

process_cells = [remove_fake_headers, remove_hidden, remove_empty]
process_cell  = [hide_cells, remove_widget_state, treat_backticks, add_jekyll_notes, convert_links]

def _find_file(cells):
    "Find in `cells` if a __file__ is defined."
    pat = re.compile(r'^__file__\s*=\s*(\S*)\s*', re.MULTILINE)
    for cell in cells:
        if cell['cell_type']=='code' and re.search(pat, cell['source']):
            return re.search(pat, cell['source']).groups()[0]

def convert_nb(fname, dest_path='docs'):
    "Convert a notebook `fname` to html file in `dest_path`."
    fname = Path(fname).absolute()
    nb = read_nb(fname)
    cls_lvl = find_default_level(nb['cells'])
    _name = _find_file(nb['cells'])
    nb['cells'] = compose(*process_cells,partial(add_show_docs, cls_lvl=cls_lvl))(nb['cells'])
    nb['cells'] = [compose(partial(copy_images, fname=fname, dest=dest_path), *process_cell)(c)
                    for c in nb['cells']]
    fname = Path(fname).absolute()
    dest_name = '.'.join(fname.with_suffix('.html').name.split('_')[1:])
    meta_jekyll = get_metadata(nb['cells'])
    meta_jekyll['nb_path'] = f'{fname.parent.name}/{fname.name}'
    nb = execute_nb(nb, name=_name)
    nb['cells'] = [clean_exports(c) for c in nb['cells']]
    with open(f'{dest_path}/{dest_name}','w') as f:
        f.write(_exporter().from_notebook_node(nb, resources=meta_jekyll)[0])

def convert_all(path='.', dest_path='docs', force_all=False):
    "Convert all notebooks in `path` to html files in `dest_path`."
    path = Path(path)
    changed_cnt = 0
    for fname in path.glob("*.ipynb"):
        # only rebuild modified files
        if fname.name.startswith('_'): continue
        fname_out = Path(dest_path)/'.'.join(fname.with_suffix('.html').name.split('_')[1:])
        if not force_all and fname_out.exists() and os.path.getmtime(fname) < os.path.getmtime(fname_out):
            continue
        print(f"converting: {fname} => {fname_out}")
        changed_cnt += 1
        try: convert_nb(fname, dest_path=dest_path)
        except: print("Failed")
    if changed_cnt==0: print("No notebooks were modified")