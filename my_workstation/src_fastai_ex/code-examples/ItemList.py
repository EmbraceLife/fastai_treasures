# %% markdown
# We can get a little glimpse of how `ItemList`'s basic attributes and methods behave with the following code examples.
# %%
from fastai.vision import *
# %%
path_data = untar_data(URLs.MNIST_TINY)
# %%
il_data = ItemList.from_folder(path_data, extensions=['.csv'])
# %% markdown
# When executing `il_data`, it is `il_data.__repr__()` working under the hood. (when `ItemList.__repr__` is not available, `built_in` function `repr(il_data)` will work instead.)
# %%
il_data
# %%
il_data.__repr__()
# %%
repr(il_data)
# %% markdown
# Here is how to access the path of `ItemList` and the actual files or `items` in the path.
# %%
il_data.path
# %%
il_data.items
# %% markdown
# `len(il_data)` is equivalent to and made possible by `il_data.__len__()`.
# %%
len(il_data)
# %%
il_data.__len__()
# %% markdown
# `il_data[idx]` is equivalent to and made possible by `il_data.__getitem__(idx)`, which uses `il_data.get(idx)`. (But for `il_data.get(idx)`, `idx` has to be integer.)
# %%
il_data.__getitem__(1.0)
# %%
il_data[1.0]
# %%
il_data.get(1)
# %% markdown
# With `il_data.new` we can make a new `ItemList` sharing the same attributes included in `il_data.new_copy`. The new object has a different reference even when they share the same `items`.
# %%
il_data_new = il_data.new(il_data.items); il_data_new
# %%
hash(il_data)
# %%
hash(il_data_new)
# %%
il_data == il_data_new
# %% markdown
# With `il_data.add` we can perform in_place concatenate another `ItemList` object.
# %%
il_data_new2 = il_data.add(il_data_new); il_data_new2
# %%
il_data == il_data_new2
# %%
il_data_new2 == il_data_new
# %%
