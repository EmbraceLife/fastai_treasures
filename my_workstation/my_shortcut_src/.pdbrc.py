"""
This is an example configuration file for pdb++.
Actually, it is what the author uses daily :-). Put it into ~/.pdbrc.py to use
it.
"""

import readline
import pdb

class Config(pdb.DefaultConfig):

    filename_color = pdb.Color.yellow

    highlight = True
    sticky_by_default = True
    line_number_color = pdb.Color.red
    filename_color = pdb.Color.yellow
    use_pygments = True
    bg = 'light'
    current_line_color = 1 # white arrow




