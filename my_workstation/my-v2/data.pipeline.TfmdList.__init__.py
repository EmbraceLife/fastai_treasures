from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import *

@docs
class TfmdList(GetAttr):
    """
    purpose:
    - why need `TfmdList` given `Pipeline` also handling multiple tfms?
    1. `Pipeline` primarily creates and deals with `tfms`
    2. `TfmdList` primarily does application to `items`

    oneliner:
    - A transform applied to a collection of `items`"

    steps:
    - `@docs`
        1. to integrate docs into the class as dict
    - `GetAttr`
        1. super class to `TfmdList`
        2. borrow 3 methods `decode`, `__call__`, `show` from Pipeline or Transform
    """

    # need some extra methods from elsewhere (not defined in this class)
    _xtra = 'decode __call__ show'.split()
    # @docs, cls._docs together make `add_docs` automatic
    # _docs = dict(setup="Transform setup with self",
    #              decode_at="Decoded item at `idx`",
    #              show_at="Show item at `idx`",
    #              subset="New `TfmdList` that only includes items at `idxs`")
    _docs = {}

    # prepare for the create of such an instance, what are needed?
    def __init__(self, items, tfm, do_setup=True):
        """
        purpose:
        - What special about TfmdList?
            a. really apply tfms to data (TfmOver, Pipeline, Transform are just preparation)
            b. do `setup()` at __init__, not a seperate step
            c. make sure all tfms are either Transform or Pipeline

        steps:
        1. differ from Pipeline, we need to deal with `items`, so put them under management of `L`
        2. to tranform, we need either `Transform` or `Pipeline` instances
        3. why don't we do the other `setup` here too, instead of another separate step?
        """
        self.items = L(items)
        self.default = self.tfm = make_tfm(tfm)
        if do_setup: self.setup()
