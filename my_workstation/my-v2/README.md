<!-- TOC -->

- [Fastai-v2 Docs on Each Item](#fastai-v2-docs-on-each-item)
  - [key terms to note](#key-terms-to-note)
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

<!-- /TOC -->
# Fastai-v2 Docs on Each Item

## key terms to note
- search "doc_improve:" with vim Ag to see my proposed source improvements in the source files below
- search "make_uncool:" with vim Ag to see how clean and compact official source code is and how to make it uncool for debugging
- search "not_finished": for official source but unfinished properly

## local.core module

### `newchk`
[core.newchk](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.newchk.py)
> enable a class to create a new instance (normal) or return the input if the input is already an instance (new feature)
<img src="https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/images/core.newchk.png" alt="newchk" width="700"/>

### `patch`
[core.patch](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.patch.py)
> enable a function to add itself to the Class of its first parameter

### `chk`
[core.chk](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.chk.py)
> enable a function to check on its parameters types

### `ls`
[core.ls](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.ls.py)
> enable a Path object with a new method to check its contents on the immediate level

### `tensor`
[core.tensor](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.tensor.py)
> put array-like, list, tuple, or just a few numbers into an tensor

### `tensor.ndim`
[core.tensor.ndim](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.tensor.ndim.py)
> add `ndim` as a property to any tensor object to return num of dimensions

### `add_docs`
[core.add_docs](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.add_docs.py)
> to add docs for Class and methods and report which has no docs yet

### `docs`
[core.docs](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.docs.py)
> to enable a Class to set up its docs (unfinished by official source yet)


### `custom_dir`, `GetAttr`
[core.custom_dir, core.GetAttr](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.getattr.py)
> 1. enable a subclass to take all its methods into its `__dir__` using `custom_dir`
> 2. access additional methods from `_xtra` using `__getattr__`

### `is_iter`
[core.is_iter](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.is_iter.py)
> to check anything is iterable or not, but Rank 0 tensors in PyTorch is not iterable

### `coll_repr`
[core.coll_repr](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.coll_repr.py)
> to print out a collection under 10 items

### `_listify`
[core._listify](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core._listify.py)
> turn everything into a list

### `_mask2idxs`
[core._mask2idxs](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core._mask2idxs.py)
> make indexes or binary indexes

### `L`
[core.L](https://github.com/EmbraceLife/fastai_docs/blob/my-v2/my-docs/core.L.py)
> the most easy-to-use and powerful list class with all the utils needed
