from local.imports import *
from local.test import *
from local.core import *
from local.notebook.showdoc import show_doc

from local.data.pipeline import *


@patch
def setup(cls:TfmdList):
      """
      purpose:
      - it is asked to do `setup` on `Pipeline` and `Transform` level
        - if it is a Pipeline, `pipeline.setup` will sort `tfms` by `order`
      - and set `prev` based on the order of Transforms, also
      - get Transforms from `self._tfms` to `self.tfms`
      - second `transform.setup` will make `_is_setup`, `_done_setup` true, and nothing else
      - Note: on Pipeline and Transform level, see args `setup(TfmdList)`
      - the full process:
          `TfmdList.setup()`=> `Pipeline.setup(tfmdlist as item)` inherit without overwritten from `Transform.setup(items)` => `Pipeline.setups(items)` inherit and overwritten => `Pipeline.add(tfms, items)` to order all tfms and loop through them for each tfm setup => `Transform.setup(items)` (turn `_is_setup` and `_done_setup` True) => `Transform.setups(items)` (pass) or other overwritten funcs
      """
      getattr(cls.tfm,'setup',noop)(cls)

show_doc(TfmdList.setup)

tfm = Pipeline(tfms=[operator.neg, float])
make_tfm(tfm)._tfms
t = TfmdList([1,2,3], tfm, do_setup=True)

tfm = [operator.neg, float]
make_tfm(tfm)._tfms
t = TfmdList([1,2,3], tfm, do_setup=True)

tfm = float
make_tfm(tfm)
t = TfmdList([1,2,3], tfm, do_setup=True)
