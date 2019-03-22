
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#文档改进" data-toc-modified-id="文档改进-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>文档改进</a></span></li><li><span><a href="#所需library" data-toc-modified-id="所需library-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>所需library</a></span></li><li><span><a href="#数据地址" data-toc-modified-id="数据地址-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>数据地址</a></span></li><li><span><a href="#创建DataBunch" data-toc-modified-id="创建DataBunch-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>创建DataBunch</a></span></li><li><span><a href="#构建模型" data-toc-modified-id="构建模型-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>构建模型</a></span></li><li><span><a href="#freeze_to-源代码" data-toc-modified-id="freeze_to-源代码-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>freeze_to 源代码</a></span></li><li><span><a href="#探查Resnet18-的layer-groups和BN与其他含参数层的数量" data-toc-modified-id="探查Resnet18-的layer-groups和BN与其他含参数层的数量-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>探查Resnet18 的layer groups和BN与其他含参数层的数量</a></span></li><li><span><a href="#查看某一个layer" data-toc-modified-id="查看某一个layer-8"><span class="toc-item-num">8&nbsp;&nbsp;</span>查看某一个layer</a></span></li><li><span><a href="#BN-classes" data-toc-modified-id="BN-classes-9"><span class="toc-item-num">9&nbsp;&nbsp;</span>BN classes</a></span></li><li><span><a href="#requires_grad如何使用" data-toc-modified-id="requires_grad如何使用-10"><span class="toc-item-num">10&nbsp;&nbsp;</span>requires_grad如何使用</a></span></li><li><span><a href="#freeze_to(0)-==-unfreeze()" data-toc-modified-id="freeze_to(0)-==-unfreeze()-11"><span class="toc-item-num">11&nbsp;&nbsp;</span>freeze_to(0) == unfreeze()</a></span></li><li><span><a href="#freeze的源代码" data-toc-modified-id="freeze的源代码-12"><span class="toc-item-num">12&nbsp;&nbsp;</span>freeze的源代码</a></span></li><li><span><a href="#assert的用法" data-toc-modified-id="assert的用法-13"><span class="toc-item-num">13&nbsp;&nbsp;</span>assert的用法</a></span></li><li><span><a href="#unfreeze的源代码" data-toc-modified-id="unfreeze的源代码-14"><span class="toc-item-num">14&nbsp;&nbsp;</span>unfreeze的源代码</a></span></li></ul></div>

#### 文档改进

The `freeze_to` source code can be understood as the following pseudo-code:
```python
def freeze_to(self, n:int)->None:
    for g in self.layer_groups[:n]: freeze 
    for g in self.layer_groups[n:]: unfreeze
```    
In other words, for example, `freeze_to(1)` is to freeze layer group 0 and unfreeze the rest layer groups, and `freeze_to(3)` is to freeze layer groups 0, 1, and 2 but unfreeze the rest layer groups (if there are more layer groups left).       

Both `freeze` and `unfreeze` [sources](https://github.com/fastai/fastai/blob/master/fastai/basic_train.py#L216) are defined using `freeze_to`:    
- When we say `freeze`, we mean that in the specified layer groups the `requires_grad` of all layers with weights (except BatchNorm layers) are set `False`, so the layer weights won't be updated during training.     
- when we say `unfreeze`, we mean that in the specified layer groups the `requires_grad` of all layers with weights (except BatchNorm layers) are set `True`, so the layer weights will be updated during training.

You can experiment `freeze_to`, `freeze` and `unfreeze` with the following experiment.

#### 所需library


```python
import fastai.vision as fv
```


```python
fv.__version__
```




    '1.0.48'



#### 数据地址


```python
path_test =  fv.Path('/kaggle/input/test');
path_train = fv.Path('/kaggle/input/train'); path_train.ls()
```




    [PosixPath('/kaggle/input/train/Fat Hen'),
     PosixPath('/kaggle/input/train/Black-grass'),
     PosixPath('/kaggle/input/train/Cleavers'),
     PosixPath('/kaggle/input/train/Small-flowered Cranesbill'),
     PosixPath('/kaggle/input/train/Sugar beet'),
     PosixPath('/kaggle/input/train/Common Chickweed'),
     PosixPath('/kaggle/input/train/Maize'),
     PosixPath('/kaggle/input/train/Loose Silky-bent'),
     PosixPath('/kaggle/input/train/Common wheat'),
     PosixPath('/kaggle/input/train/Scentless Mayweed'),
     PosixPath('/kaggle/input/train/Shepherds Purse'),
     PosixPath('/kaggle/input/train/Charlock')]



#### 创建DataBunch


```python
fv.np.random.seed(1)

### 创建DataBunch

data = fv.ImageDataBunch.from_folder(path_train,
                                  test=path_test, 
                                  ds_tfms=fv.get_transforms(),
                                  valid_pct=0.25,
                                  size=128, 
                                  bs=32,
                                  num_workers=0)
data.normalize(fv.imagenet_stats)
data
```




    ImageDataBunch;
    
    Train: LabelList (3563 items)
    x: ImageList
    Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128)
    y: CategoryList
    Fat Hen,Fat Hen,Fat Hen,Fat Hen,Fat Hen
    Path: /kaggle/input/train;
    
    Valid: LabelList (1187 items)
    x: ImageList
    Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128)
    y: CategoryList
    Sugar beet,Loose Silky-bent,Loose Silky-bent,Sugar beet,Charlock
    Path: /kaggle/input/train;
    
    Test: LabelList (794 items)
    x: ImageList
    Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128),Image (3, 128, 128)
    y: EmptyLabelList
    ,,,,
    Path: /kaggle/input/train



#### 构建模型


```python
learn = fv.cnn_learner(data, 
                      fv.models.resnet18, 
                      metrics=fv.error_rate,
                      model_dir="/kaggle/working/")
```

    Downloading: "https://download.pytorch.org/models/resnet18-5c106cde.pth" to /tmp/.torch/models/resnet18-5c106cde.pth
    100%|██████████| 46827520/46827520 [00:00<00:00, 57425711.60it/s]



```python
learn.save('start')
!ls .
```

    __notebook__.ipynb  __output__.json  start.pth


#### freeze_to 源代码

```python
learn.freeze_to??


Signature: learn.freeze_to(n:int) -> None
Source:   
    def freeze_to(self, n:int)->None:
        "Freeze layers up to layer group `n`."
        for g in self.layer_groups[:n]:
            for l in g:
                if not self.train_bn or not isinstance(l, bn_types): requires_grad(l, False)
        for g in self.layer_groups[n:]: requires_grad(g, True)
        self.create_opt(defaults.lr)
File:      /opt/conda/lib/python3.6/site-packages/fastai/basic_train.py
Type:      method
```

#### 探查Resnet18 的layer groups和BN与其他含参数层的数量


```python
print('there are ', len(learn.layer_groups), 'layer_groups in this leaner object')
```

    there are  3 layer_groups in this leaner object



```python

for g in learn.layer_groups[:]: # 打开所有layer groups
    print(len(g), 'layers')
    # 找出所有含weights的layers
    num_trainables = fv.np.array([hasattr(l, 'weight') for l in g]).sum() 
    print(num_trainables, 'layers with weights')
    # 找出所有BN layers
    num_bn = fv.np.array([isinstance(l, fv.bn_types) for l in g]).sum()
    print(num_bn, "BN layers Not be frozen")
    print(num_trainables - num_bn, 'layers which can be frozen')
    print('')
    print(g)
```

    26 layers
    20 layers with weights
    10 BN layers Not be frozen
    10 layers which can be frozen
    
    Sequential(
      (0): Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
      (1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (2): ReLU(inplace)
      (3): MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
      (4): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (5): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (6): ReLU(inplace)
      (7): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (8): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (9): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (10): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (11): ReLU(inplace)
      (12): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (13): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (14): Conv2d(64, 128, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
      (15): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (16): ReLU(inplace)
      (17): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (18): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (19): Conv2d(64, 128, kernel_size=(1, 1), stride=(2, 2), bias=False)
      (20): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (21): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (22): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (23): ReLU(inplace)
      (24): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (25): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    )
    24 layers
    20 layers with weights
    10 BN layers Not be frozen
    10 layers which can be frozen
    
    Sequential(
      (0): Conv2d(128, 256, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
      (1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (2): ReLU(inplace)
      (3): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (4): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (5): Conv2d(128, 256, kernel_size=(1, 1), stride=(2, 2), bias=False)
      (6): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (7): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (8): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (9): ReLU(inplace)
      (10): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (11): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (12): Conv2d(256, 512, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
      (13): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (14): ReLU(inplace)
      (15): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (16): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (17): Conv2d(256, 512, kernel_size=(1, 1), stride=(2, 2), bias=False)
      (18): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (19): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (20): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (21): ReLU(inplace)
      (22): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1), bias=False)
      (23): BatchNorm2d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
    )
    10 layers
    4 layers with weights
    2 BN layers Not be frozen
    2 layers which can be frozen
    
    Sequential(
      (0): AdaptiveAvgPool2d(output_size=1)
      (1): AdaptiveMaxPool2d(output_size=1)
      (2): Flatten()
      (3): BatchNorm1d(1024, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (4): Dropout(p=0.25)
      (5): Linear(in_features=1024, out_features=512, bias=True)
      (6): ReLU(inplace)
      (7): BatchNorm1d(512, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
      (8): Dropout(p=0.5)
      (9): Linear(in_features=512, out_features=12, bias=True)
    )



```python
learn.summary()
```




    ======================================================================
    Layer (type)         Output Shape         Param #    Trainable 
    ======================================================================
    Conv2d               [1, 64, 64, 64]      9,408      False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 64, 64]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 64, 64]      0          False     
    ______________________________________________________________________
    MaxPool2d            [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     73,728     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    ReLU                 [1, 128, 16, 16]     0          False     
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     8,192      False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    ReLU                 [1, 128, 16, 16]     0          False     
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       294,912    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    ReLU                 [1, 256, 8, 8]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       32,768     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    ReLU                 [1, 256, 8, 8]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       1,179,648  False     
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    ReLU                 [1, 512, 4, 4]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  False     
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       131,072    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  False     
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    ReLU                 [1, 512, 4, 4]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  False     
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    AdaptiveAvgPool2d    [1, 512, 1, 1]       0          False     
    ______________________________________________________________________
    AdaptiveMaxPool2d    [1, 512, 1, 1]       0          False     
    ______________________________________________________________________
    Flatten              [1, 1024]            0          False     
    ______________________________________________________________________
    BatchNorm1d          [1, 1024]            2,048      True      
    ______________________________________________________________________
    Dropout              [1, 1024]            0          False     
    ______________________________________________________________________
    Linear               [1, 512]             524,800    True      
    ______________________________________________________________________
    ReLU                 [1, 512]             0          False     
    ______________________________________________________________________
    BatchNorm1d          [1, 512]             1,024      True      
    ______________________________________________________________________
    Dropout              [1, 512]             0          False     
    ______________________________________________________________________
    Linear               [1, 12]              6,156      True      
    ______________________________________________________________________
    
    Total params: 11,710,540
    Total trainable params: 543,628
    Total non-trainable params: 11,166,912



#### 查看某一个layer


```python
l = learn.layer_groups[0][0]; l 
```




    Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)




```python
learn.train_bn
```




    True



#### BN classes


```python
print(fv.bn_types)
isinstance(l, fv.bn_types)
```

    (<class 'torch.nn.modules.batchnorm.BatchNorm1d'>, <class 'torch.nn.modules.batchnorm.BatchNorm2d'>, <class 'torch.nn.modules.batchnorm.BatchNorm3d'>)





    False



#### requires_grad如何使用

fv.requires_grad?

```python
Signature: fv.requires_grad(m:torch.nn.modules.module.Module, b:Union[bool, NoneType]=None) -> Union[bool, NoneType]
Docstring: If `b` is not set return `requires_grad` of first param, else set `requires_grad` on all params as `b`
File:      /opt/conda/lib/python3.6/site-packages/fastai/torch_core.py
Type:      function
```


```python
fv.requires_grad(l, False)
```

#### freeze_to(0) == unfreeze()


```python
learn.freeze_to(0) # freeze layer group before group 0
learn.summary()
```




    ======================================================================
    Layer (type)         Output Shape         Param #    Trainable 
    ======================================================================
    Conv2d               [1, 64, 64, 64]      9,408      True      
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 64, 64]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 64, 64]      0          False     
    ______________________________________________________________________
    MaxPool2d            [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     True      
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     True      
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     True      
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     True      
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     73,728     True      
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    ReLU                 [1, 128, 16, 16]     0          False     
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     8,192      True      
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    ReLU                 [1, 128, 16, 16]     0          False     
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       294,912    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    ReLU                 [1, 256, 8, 8]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       32,768     True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    ReLU                 [1, 256, 8, 8]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       1,179,648  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    ReLU                 [1, 512, 4, 4]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       131,072    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    ReLU                 [1, 512, 4, 4]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    AdaptiveAvgPool2d    [1, 512, 1, 1]       0          False     
    ______________________________________________________________________
    AdaptiveMaxPool2d    [1, 512, 1, 1]       0          False     
    ______________________________________________________________________
    Flatten              [1, 1024]            0          False     
    ______________________________________________________________________
    BatchNorm1d          [1, 1024]            2,048      True      
    ______________________________________________________________________
    Dropout              [1, 1024]            0          False     
    ______________________________________________________________________
    Linear               [1, 512]             524,800    True      
    ______________________________________________________________________
    ReLU                 [1, 512]             0          False     
    ______________________________________________________________________
    BatchNorm1d          [1, 512]             1,024      True      
    ______________________________________________________________________
    Dropout              [1, 512]             0          False     
    ______________________________________________________________________
    Linear               [1, 12]              6,156      True      
    ______________________________________________________________________
    
    Total params: 11,710,540
    Total trainable params: 11,710,540
    Total non-trainable params: 0




```python
learn.freeze_to(1) # freeze layer group before group 1
learn.summary()
```




    ======================================================================
    Layer (type)         Output Shape         Param #    Trainable 
    ======================================================================
    Conv2d               [1, 64, 64, 64]      9,408      False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 64, 64]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 64, 64]      0          False     
    ______________________________________________________________________
    MaxPool2d            [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    ReLU                 [1, 64, 32, 32]      0          False     
    ______________________________________________________________________
    Conv2d               [1, 64, 32, 32]      36,864     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 64, 32, 32]      128        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     73,728     False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    ReLU                 [1, 128, 16, 16]     0          False     
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     8,192      False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    ReLU                 [1, 128, 16, 16]     0          False     
    ______________________________________________________________________
    Conv2d               [1, 128, 16, 16]     147,456    False     
    ______________________________________________________________________
    BatchNorm2d          [1, 128, 16, 16]     256        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       294,912    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    ReLU                 [1, 256, 8, 8]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       32,768     True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    ReLU                 [1, 256, 8, 8]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 256, 8, 8]       589,824    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 256, 8, 8]       512        True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       1,179,648  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    ReLU                 [1, 512, 4, 4]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       131,072    True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    ReLU                 [1, 512, 4, 4]       0          False     
    ______________________________________________________________________
    Conv2d               [1, 512, 4, 4]       2,359,296  True      
    ______________________________________________________________________
    BatchNorm2d          [1, 512, 4, 4]       1,024      True      
    ______________________________________________________________________
    AdaptiveAvgPool2d    [1, 512, 1, 1]       0          False     
    ______________________________________________________________________
    AdaptiveMaxPool2d    [1, 512, 1, 1]       0          False     
    ______________________________________________________________________
    Flatten              [1, 1024]            0          False     
    ______________________________________________________________________
    BatchNorm1d          [1, 1024]            2,048      True      
    ______________________________________________________________________
    Dropout              [1, 1024]            0          False     
    ______________________________________________________________________
    Linear               [1, 512]             524,800    True      
    ______________________________________________________________________
    ReLU                 [1, 512]             0          False     
    ______________________________________________________________________
    BatchNorm1d          [1, 512]             1,024      True      
    ______________________________________________________________________
    Dropout              [1, 512]             0          False     
    ______________________________________________________________________
    Linear               [1, 12]              6,156      True      
    ______________________________________________________________________
    
    Total params: 11,710,540
    Total trainable params: 11,029,388
    Total non-trainable params: 681,152



#### freeze的源代码

```python
learn.freeze??

Signature: learn.freeze() -> None
Source:   
    def freeze(self)->None:
        "Freeze up to last layer group."
        assert(len(self.layer_groups)>1)
        self.freeze_to(-1)
        self.create_opt(defaults.lr) # also create an optimizer for learner
File:      /opt/conda/lib/python3.6/site-packages/fastai/basic_train.py
Type:      method
```


```python
len(learn.layer_groups)
```




    3



#### assert的用法


```python
assert(len([1,2])>1)
# assert(len([2])>1)
```

#### unfreeze的源代码


```python
learn.create_opt?
```

```python
learn.unfreeze??

Signature: learn.unfreeze()
Source:   
    def unfreeze(self):
        "Unfreeze entire model."
        self.freeze_to(0)
        self.create_opt(defaults.lr) # then create an optimizer for learner
File:      /opt/conda/lib/python3.6/site-packages/fastai/basic_train.py
Type:      method
```


```python

```
