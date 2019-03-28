
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"></ul></div>

[details="modules如何相互依赖和搭建整个系统"]

library 内各个modules之间的依赖关系 [官方文档](https://docs.fast.ai/index.html#Dependencies)


[/details][details="library结构图"]

由多个submodule组合而成
- transform
- data (DataBunch)
- models
- learn (optionally, such as Learner)

![dependpng](depend.png)

[/details]

[details="fastai调用哪些基础依赖库的具体内容"]

`fastai/imports/core`

[/details]

[details="fastai从torch中调用了哪些内容"]

`fastai/imports/torch`

[/details]

[details="fastai.core的目的功能"]

`fastai.core` 从 `fastai.imports.core` 中调用工具建设关键功能性函数来 format and split data

[/details]

[details="fastai.torch_core的目的功能"]
为fastai定制的处理tensor的功能函数集    
调用了 `imports.torch`, `core`, `collections.OrderedDict`, `torch.nn.parallel.DistributedDataParallel`

[/details]

[details="basic_data的目的和功能"]

```python
"`fastai.data` loads and manages datasets with `DataBunch`"
from .torch_core import *
from torch.utils.data.dataloader import default_collate

DatasetType = Enum('DatasetType', 'Train Valid Test Single Fix')
__all__ = ['DataBunch', 'DeviceDataLoader', 'DatasetType', 'load_data']

```

[/details]

[details="data_block的目的和功能"]
```python
from .torch_core import *
from .basic_data import *
from .layers import *
from numbers import Integral

__all__ = ['ItemList', 'CategoryList', 'MultiCategoryList', 'MultiCategoryProcessor'   , 'LabelList', 'ItemLists', 'get_files', 'PreProcessor', 'LabelLists', 'FloatList', 'CategoryProcessor', 'EmptyLabelList', 'MixedItem', 'MixedProcessor','MixedItemList']
```
[/details]

[details="layers的目的和功能"]
```python
"`fastai.layers` provides essential functions to building and modifying `model` architectures"
from .torch_core import *

__all__ = ['AdaptiveConcatPool2d', 'BCEWithLogitsFlat', 'BCEFlat', 'MSELossFlat', 'CrossEntropyFlat', 'Debugger',
'Flatten', 'Lambda', 'PoolFlatten', 'View', 'ResizeBatch', 'bn_drop_lin', 'conv2d', 'conv2d_trans', 'conv_layer',
'embedding', 'simple_cnn', 'NormType', 'relu', 'batchnorm_2d', 'trunc_normal_', 'PixelShuffle_ICNR', 'icnr',
'NoopLoss', 'WassersteinLoss', 'SelfAttention', 'SequentialEx', 'MergeLayer', 'res_block', 'sigmoid_range',
'SigmoidRange', 'PartialLayer', 'FlattenedLoss', 'BatchNorm1dFlat', 'LabelSmoothingCrossEntropy']

```
[/details]

[details="metrics的目的功能"]
```python
"Implements various metrics to measure training accuracy"
from .torch_core import *
from .callback import *
from .layers import *

__all__ = ['error_rate', 'accuracy', 'accuracy_thresh', 'dice', 'exp_rmspe', 'fbeta','FBeta', 'mse', 'mean_squared_error',
'mae', 'mean_absolute_error', 'rmse', 'root_mean_squared_error', 'msle', 'mean_squared_logarithmic_error',
'explained_variance', 'r2_score', 'top_k_accuracy', 'KappaScore', 'ConfusionMatrix', 'MatthewsCorreff',
'Precision', 'Recall', 'R2Score', 'ExplainedVariance', 'ExpRMSPE', 'RMSE', 'Perplexity']

```
[/details]

[details="callback的功能目的"]
```python
"Callbacks provides extensibility to the `basic_train` loop. See `train` for examples of custom callbacks."
from .basic_data import *
from .torch_core import *
import torch.distributed as dist

__all__ = ['AverageMetric', 'Callback', 'CallbackHandler', 'OptimWrapper', 'SmoothenValue', 'Scheduler', 'annealing_cos', 'CallbackList', 'annealing_exp', 'annealing_linear', 'annealing_no', 'annealing_poly']
```
[/details]

[details="basic_train的功能目的"]
```python
"Provides basic training and validation with `Learner`"
from .torch_core import *
from .basic_data import *
from .callback import *
from .data_block import *
from .utils.ipython import gpu_mem_restore
import inspect
from fastprogress.fastprogress import format_time, IN_NOTEBOOK
from time import time
from fastai.sixel import plot_sixel

__all__ = ['Learner', 'LearnerCallback', 'Recorder', 'RecordOnCPU', 'fit', 'loss_batch', 'train_epoch', 'validate', 'get_preds', 'load_learner']
```


[/details]

[details="callbacks功能目的"]  
callbacks是文件夹，下面有很多submodules.     
It (depends on basic_train) is a submodule defining various callbacks, such as for mixed precision training or 1cycle annealing;

```bash
__pycache__/
tracker.py*
__init__.py
csv_logger.py
fp16.py
general_sched.py
hooks.py
loss_metrics.py
lr_finder.py
mem.py
misc.py
mixup.py
mlflow.py
one_cycle.py
rnn.py
tensorboard.py
~
```
[/details]

[details="vision.data的目的功能"]

```python
"""
Manages data input pipeline - folderstransformbatch input. 
Includes support for classification, segmentation and bounding boxes
"""
from ..torch_core import *
from .image import *
from .transform import *
from ..data_block import *
from ..basic_data import *
from ..layers import *
from .learner import *
from torchvision import transforms as tvt

   __all__ = ['get_image_files', 'denormalize', 'get_annotations', 'ImageDataBunch', 'ImageList', 'normalize', 'normalize_funcs', 'resize_to','channel_view', 'mnist_stats', 'cifar_stats', 'imagenet_stats', 'download_images',
'verify_images', 'bb_pad_collate', 'ImageImageList', 'PointsLabelList', 'ObjectCategoryList', 'ObjectItemList', 'SegmentationLabelList','SegmentationItemList', 'PointsItemList']
```
[/details]

[details="text.data的功能目的"]

```python
"NLP data loading pipeline. Supports csv, folders, and preprocessed data."
from ..torch_core import *
from .transform import *
from ..basic_data import *
from ..data_block import *
from ..layers import *
from ..callback import Callback

__all__ = ['LanguageModelPreLoader', 'SortSampler', 'SortishSampler', 'Text   List', 'pad_collate', 'TextDataBunch',
--            'TextLMDataBunch', 'TextClasDataBunch', 'Text', 'open_text', 'To-- kenizeProcessor', 'NumericalizeProcessor',
||            'OpenFileProcessor', 'LMLabelList']

```


[/details]

[details="tabular.data功能目的"]
```python
"Data loading pipeline for structured data support. Loads from pandas DataFrame"
from ..torch_core import *
from .transform import *
from ..basic_data import *
from ..data_block import *
from ..basic_train import *
from .models import *
from pandas.api.types import is_numeric_dtype, is_categorical_dtype

__all__ = ['TabularDataBunch', 'TabularLine', 'TabularList', 
           'TabularProces   sor', 'tabular_learner']
```


[/details]


```python

```
