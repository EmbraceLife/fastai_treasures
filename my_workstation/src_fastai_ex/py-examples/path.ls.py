from fastai.vision import *
import fastai.vision as fv
path_data = untar_data(URLs.MNIST_TINY)
path_data.ls()
# Path.ls is a lambda function 
# Path.iterdir(): check subfolders except hidden ones
# Path.ls: return a list of Path objects for all immediate subfolders and files
