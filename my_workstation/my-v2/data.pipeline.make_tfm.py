from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import Transform, Item, Pipeline, _set_tupled
######################################################################
def make_tfm(tfm):
    """
    purpose:
    - why need `make_tfm`?
    1. we have `Transform` to create and deal a single `tfm`
    2. we have `Pipeline` to create and deal with a bunch of `tfms`
    3. but they are essentially made by the same material
    4. why not use a single func to create either of them?

    steps
    1. if `tfm` is already `Pipeline`, just return itself
    2. if `tfm` is a list of things, convert them to a `Pipeline`
    3. if `tfm` is a singular thing, just convert it to a `Transform`
    """
    if isinstance(tfm,Pipeline): return tfm
    return Pipeline(tfm) if is_listy(tfm) else Transform.create(tfm)

tfm = Pipeline(tfms=[operator.neg, float])
make_tfm(tfm)._tfms
tfm = [operator.neg, float]
make_tfm(tfm)._tfms
tfm = float
make_tfm(tfm)
