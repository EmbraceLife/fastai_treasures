from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

#This cell is just to make the config file compatible with current fastai
def _get_config():
    """
    purpose:
    - to return achive/data/models path of FASTAI_HOME
    - to overwrite config to default if `config_file` not exist and return
    """
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

ConfigKey = Enum('ConfigKey', 'Data Archive Model')


config = _get_config(); config
if 'data_archive_path' not in config: config['data_archive_path'] = config['data_path']
config
config_path = Path(os.getenv('FASTAI_HOME', '~/.fastai')).expanduser()
config_file,config_bak = config_path/'config.yml',config_path/'config.yml.bak'
with open(config_file, 'w') as yaml_file:
    yaml.dump(config, yaml_file, default_flow_style=False)

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
