
# Fastai-v2 Docs on Each Item

## key terms to note
- search "doc_improve:" with vim Ag to see my proposed source improvements in the source files below
- search "made_uncool:" with vim Ag to see how clean and compact official source code is and how to make it uncool for debugging
- search "not_finished": for official source but unfinished properly

## workload plan
according to class/method [indexes](https://github.com/fastai/fastai_docs/blob/master/dev/local/notebook/index.txt), there are 230+ class/methods in total.

- imports module has 2 funcs
- test module has 10+ classes/methods
- notebook.showdoc module has 19+ class/method
- notebook.export module has 27+ class/method (source from nb to py, **no need yet**)
- notebook.export2html module has 32+ class/method (nb to html, **no need yet**)
- notebook.core module has 3 funcs (check code running in colab, ipython, nb, easy but **no need yet**)
- local.core module has 31+ classes/methods
- data.pipeline module has 8+ classes/methods
- data.external module has 5+

# imports module (done)

<details><summary>level 1</summary>
<p>

### internals    
[imports.internals](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.internals.py)  

  <details><summary>oneliner</summary>
  <p>
  see built-in python modules fully imported and partly imported for v2
  </p>
  </details>

### externals
[imports.externals](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.externals.py)
<details><summary>oneliner</summary>
<p>
see external modules to be fully and partly imported for v2

</p>
</details>


### inspectors
[imports.inspectors](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.inspectors.py)
<details><summary>oneliner</summary>
<p>
all the functions I used the most in pdb to inspect
</p>
</details>


### `equals` and `all_equal`
[imports.all_equal](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.all_equal.py)
<details><summary>oneliner</summary>
<p>
`equals` can compare any type and `all_equal` can compare any type with same length and content

</p>
</details>


</p>
</details>


# test module (done)   

<details><summary>level 1</summary>
<p>

### `test_fail`    
[`test.test_fail`](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/test.test_fail.py)

<details><summary>oneliner</summary>
<p>
when an error/exception is unavoided, use test_fail to anticipate it
</p>
</details>

### `test`
[`test.test`](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/test.test.py)

<details><summary>oneliner</summary>
<p>
test on the use of a function to compare a and b
</p>
</details>

### `test_eq`
[`test.test_eq`](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/test.test_eq.py)
<details><summary>oneliner</summary>
<p>
test_eq = test with equals on a and b
</p>
</details>

### `test_ne`
[test.test_ne](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/test.test_ne.py)

<details><summary>oneliner</summary>
<p>
test_ne = test with nequals on a and b
</p>
</details>

### `is_close`, `test_close`    
[test.is_close, test.test_close](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/test.is_close.test_close.py)
<details><summary>oneliner</summary>
<p>
is_close = is `a` close enough to `b` within `eps`
test_close = to test `is_close` with `a`, `b` and `eps`
</p>
</details>

### `test_is`, `test_stdout`   
[test.test_is, test.test_stdout](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/test.test_is.test_stdout.py)
<details><summary>oneliner</summary>
<p>
test_is = test whether `a` is exactly `b`
test_stdout = to test whether `f()` has expected output
</p>
</details>

</p>
</details>


# notebook.showdoc module (done)  

<details><summary>level 1</summary>
<p>

### `is_enum`   
[notebook.showdoc.is_enum](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.is_enum.py)

<details><summary>oneliner</summary>
<p>
is_enum = whether the cls is enum.Enum or enum.EnumMeta
</p>
</details>

### `_get_pytorch_index` and `add_pytorch_index`
[`notebook.showdoc._get_pytorch_index` and `add_pytorch_index`](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.index.py)

<details><summary>oneliner</summary>
<p>

`_get_pytorch_index()` = show the indexes with all the pytorch functions/classes

`add_pytorch_index(func_name, url)` = add pytorch function html address onto the indexes

</p>
</details>

### `is_fastai_module`
[notebook.showdoc.is_fastai_module](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.is_fastai_module.py)

<details><summary>oneliner</summary>
<p>
`is_fastai_module(name)` = Test if `name` is a fastai module.

</p>
</details>

### `doc_link`    
[notebook.showdoc.doc_link](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.doc_link.py)

<details><summary>oneliner</summary>
<p>
`doc_link(name)` = Create link to documentation for `name`, but still strings only

</p>
</details>


### `add_doc_links`    
[notebook.showdoc.add_doc_links](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.add_doc_links.py)

<details><summary>oneliner</summary>
<p>
add_doc_links(text) = add doc link to the text where a func/class appeared

</p>
</details>

### `get_function_source`
[notebook.showdoc.get_function_source](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.get_function_source.py)

<details><summary>oneliner</summary>
<p>
get_function_source(func) = return the link to the func source online

</p>
</details>

### `get_source_link`
[notebook.showdoc.get_source_link](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.get_source_link.py)

<details><summary>oneliner</summary>
<p>
get_source_link(func, local=False, is_name=None) =     

1. return the link to notebook at specific section for the `func`     

2. `func` can be a string or object     

3. local = True, gives your local link to the notebook     

</p>
</details>

### `source_link`
[notebook.showdoc.source_link](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.source_link.py)

<details><summary>oneliner</summary>
<p>
source_link(func, is_name=None, disp=True) =

1. generate local nb link to func

2. func = a string or object

3. disp = True for link and False for string

without notebook, this is not useful.
</p>
</details>

### `type_repr`
[notebook.showdoc.type_repr](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.type_repr.py)

<details><summary>oneliner</summary>
<p>
type_repr(t) = represent type while add links to it

</p>
</details>


### `show_doc`
[notebook.showdoc.show_doc](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.show_doc.py)

<details><summary>oneliner</summary>
<p>
return the nice representation of docs and source link to nbview

personally this is most useful:

1. inline doc nice printed
2. html link to latest source and doc in nbreview
3. atom: shift+cmd+F => find the source code in my .py file to run and test


</p>
</details>

### `doc`
[notebook.showdoc.docs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/notebook.showdoc.doc.py)

<details><summary>oneliner</summary>
<p>
doc(elt) = do `show_doc` and show detailed docs link in notebook

</p>
</details>

### the remaining funcs
The remaining ones seem not have widely usage yet.

</p>
</details>

# local.core module

<details><summary>level 1</summary>
<p>

### `newchk`    
[core.newchk](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.newchk.py)

<details><summary>oneliner</summary>
<p>
enable a class to create a new instance (normal) or return the input if the input is already an instance (new feature)   

</p>
</details>

<details><summary>picsum</summary>
<p>
<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.newchk.png" alt="newchk" width="700"/>
</p>
</details>

### `patch`
[core.patch](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.patch.py)
<details><summary>oneliner</summary>
<p>
enable a function to add itself to the Class of its first parameter
</p>
</details>

<details><summary>picsum</summary>
<p>
<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.patch.png" alt="patch" width="700"/>
</p>
</details>


### `chk`
[core.chk](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.chk.py)
<details><summary>oneliner</summary>
<p>
enable a function to check on its parameters types

</p>
</details>

<details><summary>picsum</summary>
<p>

<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.chk.png" alt="patch" width="700"/>
</p>
</details>


### `ls`
[core.ls](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.ls.py)
<details><summary>oneliner</summary>
<p>
enable a Path object with a new method to check its contents on the immediate level
</p>
</details>

### `tensor`
[core.tensor](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.tensor.py)
<details><summary>oneliner</summary>
<p>
put array-like, list, tuple, or just a few numbers into an tensor
</p>
</details>


### `tensor.ndim`
[core.tensor.ndim](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.tensor.ndim.py)
<details><summary>oneliner</summary>
<p>
add `ndim` as a property to any tensor object to return num of dimensions
</p>
</details>


### `add_docs`
[core.add_docs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.add_docs.py)
<details><summary>oneliner</summary>
<p>
to add docs for Class and methods and report which has no docs yet
</p>
</details>


### `docs`
[core.docs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.docs.py)
<details><summary>oneliner</summary>
<p>
to enable a Class to set up its docs (unfinished by official source yet)
</p>
</details>

### `custom_dir`, `GetAttr`
[core.custom_dir, core.GetAttr](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.getattr.py)
<details><summary>custom_dir</summary>
<p>
enable a subclass to take all its methods into its `__dir__` using `custom_dir`
</p>
</details>

<details><summary>GetAttr</summary>
<p>
access additional methods from `_xtra` using `__getattr__`
</p>
</details>


### `is_iter`
[core.is_iter](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.is_iter.py)
<details><summary>oneliner</summary>
<p>
to check anything is iterable or not, but Rank 0 tensors in PyTorch is not iterable
</p>
</details>


### `coll_repr`
[core.coll_repr](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.coll_repr.py)
<details><summary>oneliner</summary>
<p>
to print out a collection under 10 items
</p>
</details>


### `_listify`
[core._listify](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core._listify.py)
<details><summary>oneliner</summary>
<p>
turn everything into a list
</p>
</details>


### `_mask2idxs`
[core._mask2idxs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core._mask2idxs.py)
<details><summary>oneliner</summary>
<p>
make indexes or binary indexes
</p>
</details>


### `L`
[core.L](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.L.py)
<details><summary>oneliner</summary>
<p>
the most easy-to-use and powerful list class with all the utils needed

</p>
</details>


### `defaults`
[core.defaults](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.defaults.py)
<details><summary>oneliner</summary>
<p>
create a simple namespace for storing nested values
</p>
</details>

<details><summary>picsum</summary>
<p>

<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.defaults.png" alt="defaults" width="700"/>

</p>
</details>

### `ifnone`
[core.ifnone](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.ifnone.py)
<details><summary>oneliner</summary>
<p>
refactor b if a is None else a into a function

</p>
</details>


### `noop`, `noops`
[core.noop, core.noops](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.noop.noops.py)

<details><summary>oneliner</summary>
<p>
`noop(x=None, *args, **kwargs) => do nothing to `x`, just return it

`noops(self, x, *args, **kwargs**)` => do nothing

    = to be a method of any class, since it uses `self`

</p>
</details>

### `tuplify`
[core.tuplify](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.tuplify.py)

<details><summary>oneliner</summary>
<p>
tuplify(o, use_list=False, match=None) =>

    = turn a L object into a tuple

    = use_list to split a single tensor into a tuple of 3 tensors   

</p>
</details>

###


</p>
</details>
