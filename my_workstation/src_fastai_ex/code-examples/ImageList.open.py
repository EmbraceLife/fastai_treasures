# %% markdown
# Let's get a feel of how `open` is used with the following example.
# %%
from fastai.vision import *
# %%
path_data = untar_data(URLs.PLANET_TINY); path_data.ls()
# %%
imagelistRGB = ImageList.from_folder(path_data/'train'); imagelistRGB
# %% markdown
# `open` takes only one input `fn` as `filename` in the type of `Path` or `String`.
# %%
imagelistRGB.items[10]
# %%
imagelistRGB.open(imagelistRGB.items[10])
# %%
imagelistRGB[10]
# %%
print(imagelistRGB[10])
# %% markdown
# The reason why `imagelistRGB[10]` print out an image, is because behind the scene we have `ImageList.get` calls `ImageList.open` which calls `open_image` which uses ` PIL.Image.open(fn).convert(convert_mode)` to open an image file (how we print the image), and finally turns it into an Image object with shape (3, 128, 128)
# %% markdown
# Internally, `ImageList.open` passes `ImageList.convert_mode` and `ImageList.after_open` to `open_image` to adjust the appearance of the Image object. For example, setting `convert_mode` to `L` can make images black and white.
# %%
imagelistRGB.convert_mode = 'L'
imagelistRGB.open(imagelistRGB.items[10])
