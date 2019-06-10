from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
from local.core import ls

@contextmanager
def working_directory(path):
    """
    "Change working directory to `path` and return to previous on exit."

    purpose:
    1. ever want to quickly go to a directory and come back automatically?
    2. @contextmanager decorator can help make it automatic
    3. working_directory func will perform the task 
        a. need to save current working directory
        b. go to the destination directory
        c. try something
        d. go back to previous saved working directory
    """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try: yield
    finally: os.chdir(prev_cwd)

pwd
with working_directory(Path("/Users/Natsume/Documents")):
    print(os.getcwd())
    print(Path.cwd()) # you shall see content of the directory above

pwd
