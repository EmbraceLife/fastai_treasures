from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc

########################
# why we need a simple namespace?
# how to create a nice namespace?

defaults = SimpleNamespace()

defaults.device = torch.device('cuda',0) if torch.cuda.is_available() else torch.device('cpu')

defaults.device.type
defaults.device.index

#######################
# made_uncool
if torch.cuda.is_available():
    defaults.device = torch.device('cuda',0)
else:
    defaults.device = torch.device('cpu')
