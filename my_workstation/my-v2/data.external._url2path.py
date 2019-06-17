from local.test import *
from local.imports import *
from local.core import *
from local.notebook.showdoc import show_doc
from local.data.external import ConfigKey, get_path, URLs, download_url
# ### Download in the right place
# %%
#export
def _url2path(url, c_key=ConfigKey.Archive):
    """
    purpose:
    - turn data url into file path,
    - default to a filepath in local folder, but if not actually existing
    - default to a filepath in Config folder

    Note:
    - if an actual folder is created in LOCAL_PATH, then return this local path
    - if no physical folder created in LOCAL_PATH, then return Config path
    - `shutil.move(path, path_bak)` move content from one dir to another
    """
    fname = url.split('/')[-1]
    local_path = URLs.LOCAL_PATH/('models' if c_key==ConfigKey.Model else 'data')/fname
    if local_path.exists(): return local_path
    return get_path(c_key)/fname

# Create two folder paths in LOCAL_PATH
path,path_bak = URLs.LOCAL_PATH/'data',URLs.LOCAL_PATH/'data1'
URLs.LOCAL_PATH.ls()
# if these two folder paths have actual physical folders available, delete them
if path.exists(): shutil.move(path, path_bak)
# usually no physical folder 'models' or 'data' created in LOCAL_PATH, so use Config folder
url = URLs.MNIST_TINY
test_eq(_url2path(URLs.MNIST_TINY), get_path(ConfigKey.Archive)/'mnist_tiny.tgz')
# how to quickly change the suffix of a url or filename
test_eq(_url2path(URLs.MNIST_TINY.replace('tgz', 'tar')), get_path(ConfigKey.Archive)/'mnist_tiny.tar')

test_eq(_url2path(URLs.MNIST_TINY,c_key=ConfigKey.Model), get_path(ConfigKey.Model)/'mnist_tiny.tgz')
if path_bak.exists(): shutil.move(path_bak, path)
show_doc(shutil.move)
os.makedirs('data', exist_ok=True)
download_url(f"{URLs.MNIST_TINY}.tgz", 'data/mnist_tiny.tgz')
test_eq(_url2path(URLs.MNIST_TINY), Path.cwd()/'data'/'mnist_tiny.tgz')
