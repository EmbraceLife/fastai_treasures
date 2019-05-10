from fastai.vision import *
path_data = untar_data(URLs.MNIST_TINY); path_data.ls()
il = ImageList.from_folder(path_data); il
sd = il.split_by_folder(train='train', valid='valid'); sd
func=lambda o: (o.parts if isinstance(o, Path) else o.split(os.path.sep))[-2]
ll = sd.label_from_func(func)
ll = sd.label_from_folder()
ll.train
ll.train.__repr__()
ll.train.y.classes


ll_train = sd.train.label_from_folder(from_item_lists=True)
ll_train.__class__
ll_train.y.items

ll_train.__repr__()
