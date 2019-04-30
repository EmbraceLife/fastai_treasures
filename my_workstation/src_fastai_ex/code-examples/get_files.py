import fastai.vision as fv

path_data = fv.untar_data(fv.URLs.MNIST_TINY) # small sample to try
# PosixPath('/Users/Natsume/.fastai/data/mnist_tiny')

path_data.ls()
# [PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/valid'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/labels.csv'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/test'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/history.csv'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/models'),
# PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/train')]

list_FilePath_noRecurse = fv.get_files(path_data) # recurse = False, no diving in subfolders 
list_FilePath
# [PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/labels.csv'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/history.csv')]

list_FilePath_recurse = fv.get_files(path_data, recurse=True); 
list_FilePath_recurse[:3]
# [PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/labels.csv'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/history.csv'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/valid/7/9294.png')]

list_FilePath_recurse[-2:]
# [PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/train/3/7263.png'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/train/3/7288.png')]

list_FilePath_include = fv.get_files(path_data, recurse=True, include=['test']);# use only included subfolders
list_FilePath_include[:3]
# [PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/labels.csv'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/history.csv'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/test/4605.png')]

list_FilePath_include[-3:]
# [PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/test/1605.png'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/test/2642.png'),
#  PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/test/5071.png')]
