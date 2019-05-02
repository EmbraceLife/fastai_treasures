# %% markdown
# We can get a little glimpse of how `ItemList`'s basic attributes and methods behave with the following code examples.
# %%
from fastai.vision import *
# %%
path_data = untar_data(URLs.MNIST_TINY); path_data.ls()
(path_data/'models').ls()
il_test = ItemList.from_folder(path_data, extensions=['.png'], include=['test'])
