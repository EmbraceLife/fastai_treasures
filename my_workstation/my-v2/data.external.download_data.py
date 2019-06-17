from local.test import *
from local.imports import *
from local.core import *
from local.notebook.showdoc import show_doc
from local.data.external import ConfigKey, get_path, URLs, download_url, _url2path

url = URLs.MNIST_SAMPLE
# export
def download_data(url, fname=None, c_key=ConfigKey.Archive, force_download=False):
    """
    "Download `url` to `fname`."

    purpose:
    1. usually download into Config folder
    2. unless, local folder is prepared beforehand
    3. if already downloaded, it won't download again, unless force_download
    """
    fname = Path(fname or _url2path(url, c_key=c_key))
    fname.parent.mkdir(parents=True, exist_ok=True)
    if not fname.exists() or force_download:
        print(f'Downloading {url}')
        download_url(url, fname, overwrite=force_download)
    return fname
# %% markdown
# If `fname` is None, it will default to the archive folder you have in your config file (or data, model if you specify a different `c_key`) followed by the last part of the url: for instance `URLs.MNIST_SAMPLE` is `http://files.fast.ai/data/examples/mnist_sample.tgz` and the default value for `fname` will be `~/.fastai/archive/mnist_sample.tgz`.
#
# If `force_download=True`, the file is alwayd downloaded. Otherwise, it's only when the file doesn't exists that the download is triggered.
# %%
test_eq(download_data(URLs.MNIST_SAMPLE), get_path(ConfigKey.Archive)/'mnist_sample.tgz')
test_eq(download_data(URLs.MNIST_TINY, fname=Path('mnist.tgz')), Path('mnist.tgz'))
os.remove(Path('mnist.tgz'))

tst_model = get_path(ConfigKey.Model)/'mnist_tiny.tgz'
test_eq(download_data(URLs.MNIST_TINY, c_key=ConfigKey.Model), tst_model)
os.remove(tst_model)
# %% markdown
# ### Check datasets -
# %%
#hide
#Tricking jupyter notebook to have a __file__ attribute. All _file_ will be replaced by __file__
_file_ = Path('local').absolute()/'data'/'external.py'
# %%
