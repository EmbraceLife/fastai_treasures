<!-- TOC -->

- [Fastai-v2 Docs on Each Item](#fastai-v2-docs-on-each-item)
  - [key terms to note](#key-terms-to-note)
  - [workload plan](#workload-plan)
  - [imports module](#imports-module)
    - [`internals`](#internals)
    - [`externals`](#externals)
    - [`inspectors`](#inspectors)
    - [`equals` and `all_equal`](#equals-and-all_equal)
  - [local.core module](#localcore-module)
    - [`newchk`](#newchk)
    - [`patch`](#patch)
    - [`chk`](#chk)
    - [`ls`](#ls)
    - [`tensor`](#tensor)
    - [`tensor.ndim`](#tensorndim)
    - [`add_docs`](#add_docs)
    - [`docs`](#docs)
    - [`custom_dir`, `GetAttr`](#custom_dir-getattr)
    - [`is_iter`](#is_iter)
    - [`coll_repr`](#coll_repr)
    - [`_listify`](#_listify)
    - [`_mask2idxs`](#_mask2idxs)
    - [`L`](#l)
    - [`defaults`](#defaults)
    - [`ifnone`](#ifnone)

<!-- /TOC -->

# Fastai-v2 Docs on Each Item

## key terms to note
- search "doc_improve:" with vim Ag to see my proposed source improvements in the source files below
- search "made_uncool:" with vim Ag to see how clean and compact official source code is and how to make it uncool for debugging
- search "not_finished": for official source but unfinished properly

## workload plan
- test module has 10+ classes/methods
- local.core module has 31+ classes/methods
- data.pipeline module has 8+ classes/methods
- data.external module has 5+

## imports module
### `internals`
[imports.internals](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.internals.py)
> see built-in python modules fully imported and partly imported for v2

### `externals`
[imports.externals](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.externals.py)
> see external modules to be fully and partly imported for v2

### `inspectors`
[imports.inspectors](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.inspectors.py)
> all the functions I used the most in pdb to inspect

### `equals` and `all_equal`
[imports.all_equal](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/imports.all_equal.py)
> `equals` can compare any type and `all_equal` can compare any type with same length and content

## local.core module

### `newchk`
[core.newchk](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.newchk.py)
> enable a class to create a new instance (normal) or return the input if the input is already an instance (new feature)

<details><summary>picsum</summary>
<p>
<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.newchk.png" alt="newchk" width="700"/>
</p>
</details>


### `patch`
[core.patch](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.patch.py)
> enable a function to add itself to the Class of its first parameter
<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.patch.png" alt="patch" width="700"/>

### `chk`
[core.chk](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.chk.py)
> enable a function to check on its parameters types
<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.chk.png" alt="patch" width="700"/>

### `ls`
[core.ls](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.ls.py)
> enable a Path object with a new method to check its contents on the immediate level

### `tensor`
[core.tensor](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.tensor.py)
> put array-like, list, tuple, or just a few numbers into an tensor

### `tensor.ndim`
[core.tensor.ndim](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.tensor.ndim.py)
> add `ndim` as a property to any tensor object to return num of dimensions

### `add_docs`
[core.add_docs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.add_docs.py)
> to add docs for Class and methods and report which has no docs yet

### `docs`
[core.docs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.docs.py)
> to enable a Class to set up its docs (unfinished by official source yet)


### `custom_dir`, `GetAttr`
[core.custom_dir, core.GetAttr](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.getattr.py)
> 1. enable a subclass to take all its methods into its `__dir__` using `custom_dir`
> 2. access additional methods from `_xtra` using `__getattr__`

### `is_iter`
[core.is_iter](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.is_iter.py)
> to check anything is iterable or not, but Rank 0 tensors in PyTorch is not iterable

### `coll_repr`
[core.coll_repr](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.coll_repr.py)
> to print out a collection under 10 items

### `_listify`
[core._listify](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core._listify.py)
> turn everything into a list

### `_mask2idxs`
[core._mask2idxs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core._mask2idxs.py)
> make indexes or binary indexes

### `L`
[core.L](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.L.py)
> the most easy-to-use and powerful list class with all the utils needed

### `defaults`
[core.defaults](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.defaults.py)
> create a simple namespace for storing nested values
<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.defaults.png" alt="defaults" width="700"/>

### `ifnone`
[core.ifnone](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.ifnone.py)
> refactor b if a is None else a into a function
<img src="https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/images/core.ifnone.png" alt="defaults" width="700"/>
