from fastai.vision import *
import fastai.vision as fv
path_data = untar_data(URLs.MNIST_TINY)
path_data.ls()
# don't usually use 
# `ItemList.from_folder`, `get_files`  on their own
il = ImageList.from_folder(path_data, convert_mode='L')
il.__repr__()
print(il)
