# %% markdown

# %%
from fastai.vision import *
# %%
path_data = untar_data(URLs.MNIST_TINY); path_data.ls()
# %%
itemlist = ItemList.from_folder(path_data/'test')
itemlist
# How does such output above is generated?
# behind the scenes, executing `itemlist` calls `ItemList.__repr__` which basically prints out `itemlist[0]` to `itemlist[4]`
itemlist[0]
# and `itemlist[0]` basically calls `itemlist.get(0)` which returns `itemlist.items[0]`

imagelist = ImageList.from_folder(path_data/'test')
# %%
imagelist
# How does such output above is generated?
# from `ItemList`, `ImageList` inherits `__repr__`. behind the scenes, executing `imagelist` calls `ImageList.__repr__` which basically prints out `imagelist[0]` to `imagelist[4]`
imagelist[0]
print(imagelist[0])
# and `imagelist[0]` basically calls `imagelist.get(0)` which calls `imagelist.open(imagelist.items[0])` which returns `Image` object. This is why we see 'Image (3, 28, 28)' as output of `print(imagelist[0])`
# the reason why we see printed out image as output of `imagelist[0]` is due to jupyter notebook's built-in functions.
# %%
# How `ImageList's `__init__` and `from_folder` overwrite those of `ItemList`?
# `ImageList.from_folder` add some constraints on `extensions` upon `ItemList.from_folder`, to work with image files specifically;
# `ImageList.__init__` create additional attributes like `convert_mode`, `after_open`, `c`, `sizes` upon `ItemList.__init__`;
# `convert_mode` and `sizes` in particular are necessary to make use of `ImageList.get` (which also overwrites on `ItemList.get`) and `ImageList.open`.
