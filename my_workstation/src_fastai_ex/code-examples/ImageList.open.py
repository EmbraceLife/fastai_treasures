# %% markdown
# Let's get a feel of how `open` works with the following example.
# %%
from fastai.vision import *
# %%
path_data = untar_data(URLs.PLANET_TINY); path_data.ls()
# %%
imagelistRGB = ImageList.from_folder(path_data/'train'); imagelistRGB
# %%
imagelistRGB.items[10]
# %%
imagelistRGB[10]
# %%
imagelistRGB.open(imagelistRGB.items[10])
# %%
im = imagelistRGB.open(imagelistRGB.items[10])
# %%
im
# %%
print(im)
# %%
im.__repr__()
# %% markdown
# The reason why `imagelistRGB[10]` can print an image, is `ImageList.open` called `open_image` which uses ` PIL.Image.open(fn).convert(convert_mode)` to open an image.
# %%
imagelistRGB.open(imagelistRGB.items[10])
# %% markdown
# Internally, `open` passes `ImageList.convert_mode` and `ImageList.after_open` to `open_image` to adjust the appearance of the Image object. For example, setting `convert_mode` to `L` can make images black and white.
# %%
imagelistRGB.convert_mode = 'L'
# %%
imagelistRGB.open(imagelistRGB.items[10])
# %%
x = PIL.Image.open(imagelistRGB.items[10]).convert('RGB')
