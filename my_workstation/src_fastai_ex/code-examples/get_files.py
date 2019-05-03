# %% markdown
# # get_files in plain English with demos
#
# A dataset is usually files stores within folders, a main folder and many subfolders (set `recurse`).
#
# We want to extract all files from a folder while keep their original place noted (use `_get_files`).
#
# We are only interested in non-hidden files with specific extensions, and sometimes only particular subfolders (set `extensions` and `include`).
#
# Final output is a list of FilePath objects.
#
# The following code examples give you a feel of how `get_files` behaves.
# %%
from fastai.vision import *
# %%
path_data = untar_data(URLs.MNIST_TINY)
# %%
path_data.ls()
# %% markdown
# With `recurse=False` by default, no subfolder files are made available.
# %%
list_FilePath_noRecurse = get_files(path_data)
list_FilePath_noRecurse
# %% markdown
# With `recurse=True`, all subfolder files are made available, except hidden files.
# %%
list_FilePath_recurse = get_files(path_data, recurse=True)
list_FilePath_recurse[:3]
# %%
list_FilePath_recurse[-2:]
# %% markdown
# With `extensions=['.csv']`, only files with suffix of `.csv` are made available.
# %%
list_FilePath_recurse_csv = get_files(path_data, recurse=True, extensions=['.csv'])
list_FilePath_recurse_csv
# %% markdown
# With `include=['test']`, only files in `path_data` and its subfolder `test` are made available.
# %%
list_FilePath_include = get_files(path_data, recurse=True, extensions=['.png','.jpg','.jpeg'],
                                  include=['test'])
list_FilePath_include[:3]
# %%
list_FilePath_include[-3:]
# %% markdown
# See my code example in official docs
# %%
doc(get_files)
