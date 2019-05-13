
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Improving-on-fastai-documents" data-toc-modified-id="Improving-on-fastai-documents-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Improving on fastai documents</a></span><ul class="toc-item"><li><span><a href="#The-big-picture" data-toc-modified-id="The-big-picture-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>The big picture</a></span></li><li><span><a href="#dataset-module" data-toc-modified-id="dataset-module-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>dataset module</a></span></li><li><span><a href="#data_block-module" data-toc-modified-id="data_block-module-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>data_block module</a></span></li><li><span><a href="#basic_train-module" data-toc-modified-id="basic_train-module-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>basic_train module</a></span></li><li><span><a href="#vision.data-module" data-toc-modified-id="vision.data-module-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>vision.data module</a></span></li></ul></li></ul></div>

## Improving on fastai documents
See [official docs](https://nbviewer.jupyter.org/github/fastai/fastai/tree/master/docs_src/?flush_cache=true) in jupyter notebook

This work started on my forum page [Here](https://forums.fast.ai/t/fast-ai-v3-2019/39325/92?u=daniel), and carried out on here on this repo page. 

[Search](https://github.com/fastai/fastai/pulls?page=1&q=is%3Apr+author%3AEmbraceLife+is%3Aclosed) and view all my contributions with [ReviewNB](https://www.reviewnb.com/), through those commit reviewnb pages you can raise questions on specific lines of my contrib, and I will respond as soon as I can.

Many thanks to @sgugger and @stas00 for great help and kind support!

### The big picture
- fastai module structures [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/1880/files/)
- how to use `import *` more sensibly [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/1870/files/)

### dataset module
- how does `untar_data` behave [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2009/files/)
- what does `untar_data` in a single line [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2012/files/)

### data_block module
- official docs on [data_block module](https://docs.fast.ai/data_block.html)
- how to `get_files` extract files from folders [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2017/files/)
- code examples on `get_files` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2020/files/)
- code examples on basic properites and `add` method of `ItemList` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2027/files/)
- how `ItemList.get` and `ImageList.get` differ [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2028/files/)
- how to create a new `ItemList` with `ItemList.new` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2031/files/)
- how to open an image with `ImageList.open` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2035/files/)
- how the outputs of `il` and `il[2]` are generated with `ImageList.__getitem__` and `ImageList.get` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2037/files/)
- how `convert_mode` works with `ImageList.open` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2041/files/)
- how `cmap` works with `ImageList.show` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2041/files/)
- how do `split_by_folder`, `split_by_idxs`, `split_by_list` work [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2042/files/)
- how to create an `ItemLists` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2048/files/)
- how does `ItemList.label_from_folder` work with `LabelLists` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2050/files/)
- how does `ItemList._label_from_list` work [reviewnb](https://github.com/fastai/fastai/pull/2055)
- how does `ItemLists`, `split_none` and `label_from_folder` work together [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2056/files/)
- how does `ItemList.label_from_func` work [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2063/files/)
- how does `ItemList.get_label_cls` work [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2066/files/)
- what should `a` in `index_row` be? [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2070/files/)
- how to create a label list with `CategoryList` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2071/files/)
- how to print out labels with `CategoryList.get` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2074/)
- how to create a list of labels with `LabelList` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2075/files/)
- what does `LabelList.process` do exactly [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2077/files/)
- how to get processors for dataset with `LabelLists.get_processors` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2079/files/)

### basic_train module
- how does `freeze` work and what is 'layer_group' [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/1840/files/)
- how does `freeze_to` work and how it constructs `freeze` and `unfreeze` [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/1842/files/)


### vision.data module
- how `ImageList` prints out itself [reviewnb](https://app.reviewnb.com/fastai/fastai/pull/2012/files/)


```python

```
