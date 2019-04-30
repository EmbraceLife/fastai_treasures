# How to understand ItemList

import fastai.vision as fv
path_data = fv.untar_data(fv.URLs.MNIST_TINY)
data = fv.ItemList.from_folder(path_data)
# help(fv.ItemList.__init__)
# Help on function __init__ in module fastai.data_block:
# __init__(
# self,
# items: Iterator,
# path: Union[pathlib.Path, str] = '.',
# label_cls: Callable = None,
# inner_df: Any = None,
# processor: Union[fastai.data_block.PreProcessor, Collection[fastai.data_block.PreProcessor]] = None,
# x: 'ItemList' = None,
# ignore_empty: bool = False)
