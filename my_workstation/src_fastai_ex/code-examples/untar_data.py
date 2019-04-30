import fastai.vision as fv
path_data = fv.untar_data(fv.URLs.MNIST_TINY)
# it is unlikely we will actively use untar_data in other ways
# But we can elaborate on how this function behave
# 1. once it downloaded dataset, it will not re-download it;
# 2. but if `dest` is removed, `fname` the tgz file will un-tgz dataset into `dest`
# 3. if force_download or dataset corrupted, all dataset will be removed and re-downloaded.
# also see the official docs on untar_data 
