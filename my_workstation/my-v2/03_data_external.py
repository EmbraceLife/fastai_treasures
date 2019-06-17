# %%
#default_exp data.external
# %%
#export
from local.imports import *
from local.test import *
from local.core import *
# %% markdown
# # External data
# > Helper functions to download the fastai datasets
# %% markdown
# ## Download things
# %%
# export
def download_url(url, dest, overwrite=False, pbar=None, show_progress=True, chunk_size=1024*1024,
                 timeout=4, retries=5):
    "Download `url` to `dest` unless it exists and not `overwrite`"
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
# %%
url, fname = 'http://files.fast.ai/data/examples/mnist_tiny.tgz', Path('mnist_tiny.tgz')
download_url(url, fname)
assert fname.exists()
t = os.path.getmtime(fname)
#Launching the function again doesn't trigger a download since the file is already there.
download_url(url, fname)
test_eq(t, os.path.getmtime(fname))
#But with the overwrite option, we download it again.
download_url(url, fname, overwrite=True)
test_ne(t, os.path.getmtime(fname))
# %% markdown
# Base urls
# %%
# export
class URLs():
    "Global constants for dataset and model URLs."
    LOCAL_PATH = Path.cwd()
    URL = 'http://files.fast.ai/data/examples/'
    MDL = 'http://files.fast.ai/models/'
    S3 = 'https://s3.amazonaws.com/fast-ai-'

    S3_IMAGE    = f'{S3}imageclas/'
    S3_IMAGELOC = f'{S3}imagelocal/'
    S3_NLP      = f'{S3}nlp/'
    S3_COCO     = f'{S3}coco/'
    S3_MODEL    = f'{S3}modelzoo/'

    # main datasets
    ADULT_SAMPLE        = f'{URL}adult_sample.tgz'
    BIWI_SAMPLE         = f'{URL}biwi_sample.tgz'
    CIFAR               = f'{URL}cifar10.tgz'
    COCO_SAMPLE         = f'{S3_COCO}coco_sample.tgz'
    COCO_TINY           = f'{URL}coco_tiny.tgz'
    HUMAN_NUMBERS       = f'{URL}human_numbers.tgz'
    IMDB                = f'{S3_NLP}imdb.tgz'
    IMDB_SAMPLE         = f'{URL}imdb_sample.tgz'
    ML_SAMPLE           = f'{URL}movie_lens_sample.tgz'
    MNIST_SAMPLE        = f'{URL}mnist_sample.tgz'
    MNIST_TINY          = f'{URL}mnist_tiny.tgz'
    MNIST_VAR_SIZE_TINY = f'{S3_IMAGE}mnist_var_size_tiny.tgz'
    PLANET_SAMPLE       = f'{URL}planet_sample.tgz'
    PLANET_TINY         = f'{URL}planet_tiny.tgz'
    IMAGENETTE          = f'{S3_IMAGE}imagenette.tgz'
    IMAGENETTE_160      = f'{S3_IMAGE}imagenette-160.tgz'
    IMAGENETTE_320      = f'{S3_IMAGE}imagenette-320.tgz'
    IMAGEWOOF           = f'{S3_IMAGE}imagewoof.tgz'
    IMAGEWOOF_160       = f'{S3_IMAGE}imagewoof-160.tgz'
    IMAGEWOOF_320       = f'{S3_IMAGE}imagewoof-320.tgz'

    # kaggle competitions download dogs-vs-cats -p {DOGS.absolute()}
    DOGS = f'{URL}dogscats.tgz'

    # image classification datasets
    CALTECH_101  = f'{S3_IMAGE}caltech_101.tgz'
    CARS         = f'{S3_IMAGE}stanford-cars.tgz'
    CIFAR_100    = f'{S3_IMAGE}cifar100.tgz'
    CUB_200_2011 = f'{S3_IMAGE}CUB_200_2011.tgz'
    FLOWERS      = f'{S3_IMAGE}oxford-102-flowers.tgz'
    FOOD         = f'{S3_IMAGE}food-101.tgz'
    MNIST        = f'{S3_IMAGE}mnist_png.tgz'
    PETS         = f'{S3_IMAGE}oxford-iiit-pet.tgz'

    # NLP datasets
    AG_NEWS                 = f'{S3_NLP}ag_news_csv.tgz'
    AMAZON_REVIEWS          = f'{S3_NLP}amazon_review_full_csv.tgz'
    AMAZON_REVIEWS_POLARITY = f'{S3_NLP}amazon_review_polarity_csv.tgz'
    DBPEDIA                 = f'{S3_NLP}dbpedia_csv.tgz'
    MT_ENG_FRA              = f'{S3_NLP}giga-fren.tgz'
    SOGOU_NEWS              = f'{S3_NLP}sogou_news_csv.tgz'
    WIKITEXT                = f'{S3_NLP}wikitext-103.tgz'
    WIKITEXT_TINY           = f'{S3_NLP}wikitext-2.tgz'
    YAHOO_ANSWERS           = f'{S3_NLP}yahoo_answers_csv.tgz'
    YELP_REVIEWS            = f'{S3_NLP}yelp_review_full_csv.tgz'
    YELP_REVIEWS_POLARITY   = f'{S3_NLP}yelp_review_polarity_csv.tgz'

    # Image localization datasets
    BIWI_HEAD_POSE     = f"{S3_IMAGELOC}biwi_head_pose.tgz"
    CAMVID             = f'{S3_IMAGELOC}camvid.tgz'
    CAMVID_TINY        = f'{URL}camvid_tiny.tgz'
    LSUN_BEDROOMS      = f'{S3_IMAGE}bedroom.tgz'
    PASCAL_2007        = f'{S3_IMAGELOC}pascal_2007.tgz'
    PASCAL_2012        = f'{S3_IMAGELOC}pascal_2012.tgz'

    #Pretrained models
    OPENAI_TRANSFORMER = f'{S3_MODEL}transformer.tgz'
    WT103              = f'{S3_MODEL}wt103.tgz'
    #TODO: remove this last one and make sure the mosr recent is up
    WT103_1            = f'{S3_MODEL}wt103-1.tgz'
# %% markdown
# ## Config file
# %%
# export
def _get_config():
    config_path = Path(os.getenv('FASTAI_HOME', '~/.fastai')).expanduser()
    config_file = config_path/'config.yml'
    if config_file.exists():
        with open(config_file, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            if 'version' in config and config['version'] == 1: return config
    else: config = {}
    #File inexistent or wrong version -> going to default
    config = {'data_path':    str(config_path/'data'),
              'archive_path': str(config_path/'archive'),
              'model_path':   str(config_path/'models'),
              'version':      1}
    with open(config_file, 'w') as yaml_file:
        yaml.dump(config, yaml_file, default_flow_style=False)
    return config
# %%
#This cell is just to make the config file compatible with current fastai
config = _get_config()
if 'data_archive_path' not in config: config['data_archive_path'] = config['data_path']
config_path = Path(os.getenv('FASTAI_HOME', '~/.fastai')).expanduser()
config_file,config_bak = config_path/'config.yml',config_path/'config.yml.bak'
with open(config_file, 'w') as yaml_file:
    yaml.dump(config, yaml_file, default_flow_style=False)
# %%
config_path = Path(os.getenv('FASTAI_HOME', '~/.fastai')).expanduser()
config_file,config_bak = config_path/'config.yml',config_path/'config.yml.bak'
if config_file.exists(): shutil.move(config_file, config_bak)
#Test default config
config = _get_config()
assert (config_path/'config.yml').exists()
test_eq(config, {
        'data_path':    str(config_path/'data'),
        'archive_path': str(config_path/'archive'),
        'model_path':   str(config_path/'models'),
        'version':      1
    })

#Test change in config
config['archive_path'] = '.'
with open(config_path/'config.yml', 'w') as yaml_file:
    yaml.dump(config, yaml_file, default_flow_style=False)
config = _get_config()
test_eq(config, {
        'data_path':    str(config_path/'data'),
        'archive_path': '.',
        'model_path':   str(config_path/'models'),
        'version':      1
    })

if config_bak.exists(): shutil.move(config_bak, config_file)
# %%
# export
ConfigKey = Enum('ConfigKey', 'Data Archive Model')

def get_path(c_key=ConfigKey.Data):
    return Path(_get_config()[f"{c_key.name.lower()}_path"])
# %%
config = _get_config()
test_eq(Path(config['data_path']),    get_path(ConfigKey.Data))
test_eq(Path(config['archive_path']), get_path(ConfigKey.Archive))
test_eq(Path(config['model_path']),   get_path(ConfigKey.Model))
# %% markdown
# ### Download in the right place
# %%
#export
def _url2path(url, c_key=ConfigKey.Archive):
    fname = url.split('/')[-1]
    local_path = URLs.LOCAL_PATH/('models' if c_key==ConfigKey.Model else 'data')/fname
    if local_path.exists(): return local_path
    return get_path(c_key)/fname
# %%
#hide
path,path_bak = URLs.LOCAL_PATH/'data',URLs.LOCAL_PATH/'data1'
if path.exists(): shutil.move(path, path_bak)
test_eq(_url2path(URLs.MNIST_TINY), get_path(ConfigKey.Archive)/'mnist_tiny.tgz')
test_eq(_url2path(URLs.MNIST_TINY.replace('tgz', 'tar')), get_path(ConfigKey.Archive)/'mnist_tiny.tar')
test_eq(_url2path(URLs.MNIST_TINY,c_key=ConfigKey.Model), get_path(ConfigKey.Model)/'mnist_tiny.tgz')
if path_bak.exists(): shutil.move(path_bak, path)

os.makedirs('data', exist_ok=True)
download_url(f"{URLs.MNIST_TINY}.tgz", 'data/mnist_tiny.tgz')
test_eq(_url2path(URLs.MNIST_TINY), Path.cwd()/'data'/'mnist_tiny.tgz')
# %%
# export
def download_data(url, fname=None, c_key=ConfigKey.Archive, force_download=False):
    "Download `url` to `fname`."
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
#export
def _get_check(url):
    checks = json.load(open(Path(_file_).parent/'checks.txt', 'r'))
    return checks.get(url, None)

def _check_file(fname):
    size = os.path.getsize(fname)
    with open(fname, "rb") as f:
        hash_nb = hashlib.md5(f.read(2**20)).hexdigest()
    return [size,hash_nb]
# %%
#hide
test_eq(_get_check(URLs.MNIST_SAMPLE), _check_file(_url2path(URLs.MNIST_SAMPLE)))
# %%
#export
def _add_check(url, fname):
    "Internal function to update the internal check file with `url` and check on `fname`."
    checks = json.load(open(Path(_file_).parent/'checks.txt', 'r'))
    checks[url] = _check_file(fname)
    json.dump(checks, open(Path(_file_).parent/'checks.txt', 'w'), indent=2)
# %%
#export
def untar_data(url, fname=None, dest=None, c_key=ConfigKey.Data, force_download=False):
    "Download `url` to `fname` if `dest` doesn't exist, and un-tgz to folder `dest`."
    default_dest = _url2path(url, c_key=c_key).with_suffix('')
    dest = default_dest if dest is None else Path(dest)/default_dest.name
    fname = Path(fname or _url2path(url))
    if fname.exists() and _get_check(url) and _check_file(fname) != _get_check(url):
        print("A new version of this is available, downloading...")
        force_download = True
    if force_download:
        if fname.exists(): os.remove(fname)
        if dest.exists(): shutil.rmtree(dest)
    if not dest.exists():
        fname = download_data(url, fname=fname, c_key=c_key)
        if _get_check(url) and _check_file(fname) != _get_check(url):
            print(f"File downloaded is broken. Remove {fname} and try again.")
        tarfile.open(fname, 'r:gz').extractall(dest.parent)
    return dest
# %% markdown
# `untar_data` is a convenience function for the fastai datasets, intended to work with the urls in `URLs`. You can use it with another url only if it ends with `.tgz` (otherwise the function can download it but not decompress it). For other extensions, you should use `download_data` then the necessary decompress function.
#
# If `fname` is specified, the data will be downloaded to that destination, otherwise it will default to the archive path in your config file (default `~/.fastai/archive/`) followed by the last part of your url. For instance `URLs.MNIST_SAMPLE` is `http://files.fast.ai/data/examples/mnist_sample.tgz` and the default value for `fname` will be `~/.fastai/archive/mnist_sample.tgz`.
#
# If `dest` is specified, the data will be decompressed to that folder. Otherwise, it will default to the data path (or model/archive if you specify a different `c_key`) in your config file (default `~/.fastai/data/`) followed by the last part of your url without extension. For instance `URLs.MNIST_SAMPLE` is `http://files.fast.ai/data/examples/mnist_sample.tgz` and the default value for `dest` will be `~/.fastai/data/mnist_sample`.
#
# `force_download=True` will retrigger a download, otherwise the behavior is to:
# - not do anything when `dest` exists
# - otherwise decompress `fname` to `dest` if `fname` exists
# - otherwise download then decompress `fname` to `dest`
# %%
test_eq(untar_data(URLs.MNIST_SAMPLE), get_path()/'mnist_sample')

#Test specific fname
untar_data(URLs.MNIST_TINY, fname='mnist_tiny.tgz', force_download=True)
assert Path('mnist_tiny.tgz').exists()
os.remove(Path('mnist_tiny.tgz'))

#Test specific dest
test_eq(untar_data(URLs.MNIST_TINY, dest='.'), Path('mnist_tiny'))
assert Path('mnist_tiny').exists()
shutil.rmtree(Path('mnist_tiny'))

#Test c_key
tst_model = get_path(ConfigKey.Model)/'mnist_sample'
test_eq(untar_data(URLs.MNIST_SAMPLE, c_key=ConfigKey.Model), tst_model)
assert not tst_model.with_suffix('.tgz').exists() #Archive wasn't downloaded in the models path
assert (get_path(ConfigKey.Archive)/'mnist_sample.tgz').exists() #Archive was downloaded there
shutil.rmtree(tst_model)
# %% markdown
# ## Export -
# %%
#hide
! ./notebook2script.py
# %%
