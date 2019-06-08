
# Fastai-v2 Docs on Each Item

## project goal
- know the library inside out
- plot detail logic flow diagrams for nbs to show true understanding

## key terms to note
- search "doc_improve:" with vim Ag or Atom: shift+cmd+F to see my proposed source improvements on the official source
- search "made_uncool:" with vim Ag to see how clean and compact official source code is and how to make it uncool for debugging
- search "doc_doubts": maybe the official source is problematic


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

`@chk`

> enable a function to check on its parameters types automatically

> important note: f() run inside `typechecked()`

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

> `tensor(x, *rest)` = return a tensor from many different types below

> `x` = scalar, tuple, list, array

> `rest` = a few numbers like (1,2,3)

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

> @newchk` = to make sure L(instance_L) returns the same instance

> `GetAttr` and `_xtra` = base class to steal methods of `list` to class `L`

> = get items into a list and assigned to self.items and self.default

> `use_list` = break a tensor into several

> `match` = match the length of items

> `__getitem__(self, idx)` = return individual values or L instance

> `__setitem__(self, idx, o)` = Set `idx` (can be list of indices, or mask, or int) items to `o`

> `sorted(self, key=None, reverse=False)` = return New `L` sorted by `key`. If key is str then use `attrgetter`. If key is int then use `itemgetter`."

> `def __len__(self): return len(self.items)`

> `def __delitem__(self, i): del(self.items[i])`

> `def __repr__(self): return f'{coll_repr(self)}'`

> `def __eq__(self,b): return all_equal(b,self)`

> `def __iter__(self): return (self[i] for i in range(len(self)))`

> `def __mul__ (a,b): return L(a.items*b)`

> `def __add__ (a,b): return L(a.items+_listify(b))`

> `def __radd__(a,b): return L(b)+a`

> `def __addi__(a,b): a.items += list(b); return a`

> `def mapped(self, f):    return L(map(f, self))`

> `def zipped(self):       return L(zip(*self))`

> `def itemgot(self, idx): return self.mapped(itemgetter(idx))`

> `def attrgot(self, k):   return self.mapped(lambda o:getattr(o,k,0))`

> `def tensored(self):     return self.mapped(tensor)`

> `def stack(self, dim=0): return torch.stack(list(self.tensored()), dim=dim)`

> `def cat  (self, dim=0): return torch.cat  (list(self.tensored()), dim=dim)`

</p>
</details>


### `defaults`
[core.defaults](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.defaults.py)
<details><summary>oneliner</summary>
<p>

> create a simple namespace for storing nested values

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

`ifnone(a, b)`

> refactor b if a is None else a into a function

</p>
</details>


### `noop`, `noops`
[core.noop, core.noops](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.noop.noops.py)

<details><summary>oneliner</summary>
<p>

`noop(x=None, *args, **kwargs)`

> do nothing to `x`, just return it

`noops(self, x, *args, **kwargs)`

> do nothing to `x`, just return it.

> to be a method of any class, since it uses `self`

</p>
</details>

### `tuplify`
[core.tuplify](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.tuplify.py)

<details><summary>oneliner</summary>
<p>

`tuplify(o, use_list=False, match=None)`

> turn a `L` object into a tuple

> `use_list` to split a single tensor into a tuple of 3 tensors   

</p>
</details>

### `replicate`
[core.replicate](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.replicate.py)

<details><summary>oneliner</summary>
<p>

`replicate(item,match)`

> copy `item` `match` times into a tuple

> `item` = single value, list or tuple

</p>
</details>

### `uniqueify`
[core.uniqueify](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.uniqueify.py)

<details><summary>oneliner</summary>
<p>

`uniqueify(x, sort=False, bidir=False, start=None)`

> = return a unique list

> `x` = a list of values, duplicated, and not sorted

> `sort = True` = sort the unique list

> `bidir=True` = also return a dict where the unique list are the keys

> `start=None` = if not None, then add `start` on to the unique list

</p>
</details>

### `setify`
[core.setify](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.setify.py)

<details><summary>oneliner</summary>
<p>

> `setify(o)`

> = return o if o is a set

> = return a new set from `set(L(o))`

</p>
</details>

### `is_listy`
[core.is_listy](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.is_listy.py)

<details><summary>oneliner</summary>
<p>

> `is_listy(x)` = whether `x` is instance of tuple, list, L or slice

</p>
</details>

### `range_of`

[core.range_of](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.range_of.py)

<details><summary>oneliner</summary>
<p>

> `range_of(x)` = return a list of indexes for `x`

</p>
</details>

### `mask2idxs`
[core.mask2idxs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.mask2idxs.py)

<details><summary>onelinear</summary>
<p>

>`mask2idxs(mask)` = turn mask into a list of idx/values as L object

>`mask` = tuple, list of values, strings, bools, even a tensor of list

>`mask` = can't be single value like 3, or (3), but (3,) or [3] works

</p>
</details>

### `apply`
[core.apply](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.apply.py)

<details><summary>oneliner</summary>
<p>

> `apply(func, x, *args, **kwargs)` = recursively apply func to `x`

> `func` = any func

> `x` = anything of a scalar, a list/tuple, or a dict

</p>
</details>

### `to_detach`
[core.to_detach](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.to_detach.py)

<details><summary>onelinear</summary>
<p>

> `to_detach(b, cpu=True)`

> = detach lists of tensors in `b `; put them on the CPU if `cpu=True`

</p>
</details>

### `to_half`, `to_float`
[core.to_half, core.to_float](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.to_half.to_float.py)

<details><summary>docs</summary>
<p>

> `to_half(b)` = Recursively map lists of float tensors in `b` to FP16

> `to_float(b)` = Recursively map lists of float tensors in `b` to float32

</p>
</details>

### `to_device`, `to_cpu`
[core.to_device, core.to_cpu](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.to_device.to_cpu.py)

<details><summary>docs</summary>
<p>

`to_device(b, device=defaults.device)`

> = Recursively put `b` on `device`, by default on gpu

`to_cpu(b)`

> = Recursively map lists of tensors in `b ` to the cpu

</p>
</details>

### `item_find`, `find_device`
[core.item_find, core.find_device](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.item_find.find_device.py)

<details><summary>docs</summary>
<p>

`item_find(x, idx=0)`

> = recursively dive deeper to get the idx-th item of x

> `x` = list of list or dict of dict

> `idx` = int as index working for list and dict, or not int for dict's key

> `idx` = user defined int works for the first level, lower levels controlled by default value 0


`find_device(b)`

> = Recursively search the device of `b`

> and `idx` from `item_find` is default 0 and not changeable

</p>
</details>

### `find_bs`
[core.find_bs](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.find_bs.py)

<details><summary>docs</summary>
<p>

`find_bs(b)`

> = Recursively search the batch size of `b`

> `b` = a batch of dataset

> batch_size = the shape[0] of first item of b recursively

</p>
</details>

### `compose`
[core.compose](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.compose.py)

<details><summary>docs</summary>
<p>

`compose(*funcs: Callable, order=None)`

> = wrap func around func by their positional order or specified order

> = arguments for `compose` and `funcs` can be properly passed onto

> = `L.sorted` handles with order

> = `compose()` itself run inside `@chk`, then `_inner()` will run after

> Note: how `order` are passed to `compose`

> Noet: and how `x`, `p` are passed onto `funcs`


</p>
</details>

### `mapper`

[core.mapper](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.mapper.py)

<details><summary>docs</summary>
<p>

`mapper(f)`

> = map a func onto every input of an collection

> mapper(f) is a lambda on its own

> mapper(f)(data) is how we use it

</p>
</details>

### `partialler`
[core.partialler](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.partialler.py)

<details><summary>docs</summary>
<p>

`partialler(f, *args, order=None, **kwargs)`

> = Like `functools.partial` but also copies over docstring"

> = also set `order` too

> = returns a args-specified function of `f`

</p>
</details>

### `sort_by_run`
[core.sort_by_run](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.sort_by_run.py)


<details><summary>docs</summary>
<p>


`sort_by_run(fs)`

> = rank funcs into a list based on their execution order

> `end` = index of `gs` which has `toward_end` attribut

> `inp, res` = the full fs, and empty lis

> loop through all funcs, test which is the first fun

> get the first func into `res` the list

`_is_first(f, gs)`

> = whether `f` is the first func inside `gs`

> return False if `f.run_after` is an instance of any func in `gs`

> return False if `f` is an instance of the `g.run_before` from `gs`

> except two conditions above, `f` is the first func of `gs`

`_is_instance(f, gs)`

> = check if `f` is an instance of or exact the same to any `g` from `gs`

> if `g` is a type or func, then `f` == `g` makes True returned

> if `g` is a class, then `f` is an instance of `g` makes True returned


</p>
</details>

### `add_props`
[core.add_props](https://github.com/EmbraceLife/fastai_treasures/blob/master/my_workstation/my-v2/core.add_props.py)

<details><summary>docs</summary>
<p>

`add_props(f, n=2)`

> = add properties to a class, `n` set for number of properties

> = properties difference are based on `i` from `i in range(n)`, and

> = `partial(f, i)` => if `f` is lambda then must have two args `x` and `i`


</p>
</details>


</p>
</details>
