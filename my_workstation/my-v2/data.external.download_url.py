#default_exp data.external
#export
from local.imports import *
from local.test import *
from local.core import * # if error, make sure `torch.cuda.is_available()`
from local.notebook.showdoc import show_doc
# # External data
# > Helper functions to download the fastai datasets
# ## Download things
# export
def download_url(url, dest, overwrite=False, pbar=None, show_progress=True, chunk_size=1024*1024,
                 timeout=4, retries=5):
    """
    purpose:
    1. if `desk` has content and `overwrite` is False, return nothing
    2. start to request info from a `url` with `retries`, `timeout`
    3. open `desk` and start to write data
        3.1 if `show_progress` True, create a `progress_bar`
        3.2 update the `pbar` with accumulated `chunk_size`
        3.3 `f.write(chunk)` to write the data
        3.4 if connection error raise, message how to do it manually

    Note:
    `desk`: should be a filename/path for `tgz` files
    `overwrite`: True to download again, False to now download again
    """
    if os.path.exists(dest) and not overwrite: return

    s = requests.Session()
    s.mount('http://',requests.adapters.HTTPAdapter(max_retries=retries))
    u = s.get(url, stream=True, timeout=timeout)
    try: file_size = int(u.headers["Content-Length"])
    except: show_progress = False

    with open(dest, 'wb') as f:
        nbytes = 0
        if show_progress:
            pbar = progress_bar(range(file_size), auto_update=False, leave=False, parent=pbar)
        try:
            for chunk in u.iter_content(chunk_size=chunk_size):
                nbytes += len(chunk)
                if show_progress: pbar.update(nbytes)
                f.write(chunk)
        except requests.exceptions.ConnectionError as e:
            fname = url.split('/')[-1]
            from fastai.datasets import Config
            data_dir = dest.parent
            print(f'\n Download of {url} has failed after {retries} retries\n'
                  f' Fix the download manually:\n'
                  f'$ mkdir -p {data_dir}\n'
                  f'$ cd {data_dir}\n'
                  f'$ wget -c {url}\n'
                  f'$ tar -zxvf {fname}\n'
                  f' And re-run your code once the download is successful\n')

url, fname = 'http://files.fast.ai/data/examples/mnist_tiny.tgz', Path('mnist_tiny.tgz')
download_url(url, fname)
assert fname.exists() # make sure the file actually exists
t = os.path.getmtime(fname);t # report the last file modification time
#Launching the function again doesn't trigger a download since the file is already there.
download_url(url, fname)
test_eq(t, os.path.getmtime(fname))
#But with the overwrite option, we download it again.
download_url(url, fname, overwrite=True)
test_ne(t, os.path.getmtime(fname))
