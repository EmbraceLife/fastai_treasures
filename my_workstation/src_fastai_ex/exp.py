from fastai.vision import *
path_data = untar_data(URLs.MNIST_TINY); path_data.ls()
il = ImageList.from_folder(path_data); il
sd = il.split_by_folder(train='train', valid='valid'); sd
func=lambda o: (o.parts if isinstance(o, Path) else o.split(os.path.sep))[-2]
ll = sd.label_from_func(func)
ll = sd.label_from_folder()
ll.train.y[-3]
items = ll.train.items
cl = CategoryList(items)
cl.filter_missing_y
cl.__repr__()
