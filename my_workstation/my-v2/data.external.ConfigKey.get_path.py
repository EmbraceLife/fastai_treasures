from local.imports import *
from local.test import *
from local.core import *
from local.data.external import _get_config
# export
ConfigKey = Enum('ConfigKey', 'Data Archive Model')

def get_path(c_key=ConfigKey.Data):
    return Path(_get_config()[f"{c_key.name.lower()}_path"])

config = _get_config(); config
test_eq(Path(config['data_path']),    get_path(ConfigKey.Data))
test_eq(Path(config['archive_path']), get_path(ConfigKey.Archive))
test_eq(Path(config['model_path']),   get_path(ConfigKey.Model))

ConfigKey.Archive.name.lower()
ConfigKey.Model.name.lower()
