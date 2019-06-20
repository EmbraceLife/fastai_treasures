from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc


def num_cpus():
    "Get number of cpus"
    try:                   return len(os.sched_getaffinity(0))
    except AttributeError: return os.cpu_count()

defaults.cpus = min(16, num_cpus())
