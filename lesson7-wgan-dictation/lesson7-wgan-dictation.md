
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#三行魔法代码" data-toc-modified-id="三行魔法代码-0.0.1"><span class="toc-item-num">0.0.1&nbsp;&nbsp;</span>三行魔法代码</a></span></li><li><span><a href="#所需library" data-toc-modified-id="所需library-0.0.2"><span class="toc-item-num">0.0.2&nbsp;&nbsp;</span>所需library</a></span></li><li><span><a href="#下载数据（部分数据，源于Kaggle）" data-toc-modified-id="下载数据（部分数据，源于Kaggle）-0.0.3"><span class="toc-item-num">0.0.3&nbsp;&nbsp;</span>下载数据（部分数据，源于Kaggle）</a></span></li></ul></li></ul></li><li><span><a href="#LSun-bedroom-data" data-toc-modified-id="LSun-bedroom-data-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>LSun bedroom data</a></span><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#如何构建databunch" data-toc-modified-id="如何构建databunch-1.0.1"><span class="toc-item-num">1.0.1&nbsp;&nbsp;</span>如何构建databunch</a></span></li><li><span><a href="#从小尺寸数据开始训练" data-toc-modified-id="从小尺寸数据开始训练-1.0.2"><span class="toc-item-num">1.0.2&nbsp;&nbsp;</span>从小尺寸数据开始训练</a></span></li></ul></li></ul></li><li><span><a href="#Models" data-toc-modified-id="Models-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Models</a></span><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#如何理解GAN-的工作原理" data-toc-modified-id="如何理解GAN-的工作原理-2.0.1"><span class="toc-item-num">2.0.1&nbsp;&nbsp;</span>如何理解GAN 的工作原理</a></span></li><li><span><a href="#如何生成简单的generator-and-critic" data-toc-modified-id="如何生成简单的generator-and-critic-2.0.2"><span class="toc-item-num">2.0.2&nbsp;&nbsp;</span>如何生成简单的generator and critic</a></span></li><li><span><a href="#如何构建wgan-learner" data-toc-modified-id="如何构建wgan-learner-2.0.3"><span class="toc-item-num">2.0.3&nbsp;&nbsp;</span>如何构建wgan learner</a></span></li><li><span><a href="#查看模型结果" data-toc-modified-id="查看模型结果-2.0.4"><span class="toc-item-num">2.0.4&nbsp;&nbsp;</span>查看模型结果</a></span></li></ul></li></ul></li></ul></div>

[WGAN explained](https://ytcropper.com/cropped/9s5c8c82395554d)

#### 三行魔法代码


```python
%reload_ext autoreload
%autoreload 2
%matplotlib inline
```

#### 所需library


```python
from fastai.vision import *
from fastai.vision.gan import *
```

#### 下载数据（部分数据，源于Kaggle）

## LSun bedroom data

For this lesson, we'll be using the bedrooms from the [LSUN dataset](http://lsun.cs.princeton.edu/2017/). The full dataset is a bit too large so we'll use a sample from [kaggle](https://www.kaggle.com/jhoward/lsun_bedroom).


```python
path = untar_data(URLs.LSUN_BEDROOMS)
```

#### 如何构建databunch

We then grab all the images in the folder with the data block API. We don't create a validation set here for reasons we'll explain later. It consists of random noise of size 100 by default (can be changed below) as inputs and the images of bedrooms as targets. That's why we do `tfm_y=True` in the transforms, then apply the normalization to the ys and not the xs.


```python
def get_data(bs, size):
    return (GANItemList.from_folder(path, noise_sz=100) # noise as inputs, image as targets
               .no_split()
               .label_from_func(noop) # what is noop?
               .transform(tfms=[[crop_pad(size=size, row_pct=(0,1), col_pct=(0,1))], []], 
                          size=size, 
                          tfm_y=True) # transform to y not x
               .databunch(bs=bs)
               .normalize(stats = [torch.tensor([0.5,0.5,0.5]), torch.tensor([0.5,0.5,0.5])], 
                          do_x=False, do_y=True)) # normalize y not x
```

#### 从小尺寸数据开始训练

We'll begin with a small side and use gradual resizing.


```python
data = get_data(128, 64)
```


```python
data.show_batch(rows=5)
```


![png](output_16_0.png)


## Models

#### 如何理解GAN 的工作原理

GAN stands for [Generative Adversarial Nets](https://arxiv.org/pdf/1406.2661.pdf) and were invented by Ian Goodfellow. The concept is that we will train two models at the same time: a generator and a critic. The generator will try to make new images similar to the ones in our dataset, and the critic will try to classify real images from the ones the generator does. The generator returns images, the critic a single number (usually 0. for fake images and 1. for real ones).

We train them against each other in the sense that at each step (more or less), we:
1. Freeze the generator and train the critic for one step by:
  - getting one batch of true images (let's call that `real`)
  - generating one batch of fake images (let's call that `fake`)
  - have the critic evaluate each batch and compute a loss function from that; the important part is that it rewards positively the detection of real images and penalizes the fake ones
  - update the weights of the critic with the gradients of this loss
  
  
2. Freeze the critic and train the generator for one step by:
  - generating one batch of fake images
  - evaluate the critic on it
  - return a loss that rewards posisitivly the critic thinking those are real images; the important part is that it rewards positively the detection of real images and penalizes the fake ones
  - update the weights of the generator with the gradients of this loss
  
Here, we'll use the [Wassertein GAN](https://arxiv.org/pdf/1701.07875.pdf).

We create a generator and a critic that we pass to `gan_learner`. The noise_size is the size of the random vector from which our generator creates images.

#### 如何生成简单的generator and critic


```python
generator = basic_generator(in_size=64, n_channels=3, n_extra_layers=1)
critic    = basic_critic   (in_size=64, n_channels=3, n_extra_layers=1)
```

#### 如何构建wgan learner


```python
learn = GANLearner.wgan(data, generator, critic, switch_eval=False,
                        opt_func = partial(optim.Adam, betas = (0.,0.99)), wd=0.)
```


```python
learn.fit(30,2e-4)
```


Total time: 1:54:23 <p><table style='width:300px; margin-bottom:10px'>
  <tr>
    <th>epoch</th>
    <th>train_loss</th>
    <th>gen_loss</th>
    <th>disc_loss</th>
  </tr>
  <tr>
    <th>1</th>
    <th>-0.842719</th>
    <th>0.542895</th>
    <th>-1.086206</th>
  </tr>
  <tr>
    <th>2</th>
    <th>-0.799776</th>
    <th>0.539448</th>
    <th>-1.067940</th>
  </tr>
  <tr>
    <th>3</th>
    <th>-0.738768</th>
    <th>0.538581</th>
    <th>-1.015152</th>
  </tr>
  <tr>
    <th>4</th>
    <th>-0.718174</th>
    <th>0.484403</th>
    <th>-0.943485</th>
  </tr>
  <tr>
    <th>5</th>
    <th>-0.570070</th>
    <th>0.428915</th>
    <th>-0.777247</th>
  </tr>
  <tr>
    <th>6</th>
    <th>-0.545130</th>
    <th>0.413026</th>
    <th>-0.749381</th>
  </tr>
  <tr>
    <th>7</th>
    <th>-0.541453</th>
    <th>0.389443</th>
    <th>-0.719322</th>
  </tr>
  <tr>
    <th>8</th>
    <th>-0.469548</th>
    <th>0.356602</th>
    <th>-0.642670</th>
  </tr>
  <tr>
    <th>9</th>
    <th>-0.434924</th>
    <th>0.329100</th>
    <th>-0.598782</th>
  </tr>
  <tr>
    <th>10</th>
    <th>-0.416448</th>
    <th>0.301526</th>
    <th>-0.558442</th>
  </tr>
  <tr>
    <th>11</th>
    <th>-0.389224</th>
    <th>0.292355</th>
    <th>-0.532662</th>
  </tr>
  <tr>
    <th>12</th>
    <th>-0.361795</th>
    <th>0.266539</th>
    <th>-0.494872</th>
  </tr>
  <tr>
    <th>13</th>
    <th>-0.363674</th>
    <th>0.245725</th>
    <th>-0.475951</th>
  </tr>
  <tr>
    <th>14</th>
    <th>-0.318343</th>
    <th>0.227446</th>
    <th>-0.432148</th>
  </tr>
  <tr>
    <th>15</th>
    <th>-0.309221</th>
    <th>0.203628</th>
    <th>-0.417945</th>
  </tr>
  <tr>
    <th>16</th>
    <th>-0.300667</th>
    <th>0.213194</th>
    <th>-0.401034</th>
  </tr>
  <tr>
    <th>17</th>
    <th>-0.282622</th>
    <th>0.187128</th>
    <th>-0.381643</th>
  </tr>
  <tr>
    <th>18</th>
    <th>-0.283902</th>
    <th>0.156653</th>
    <th>-0.374541</th>
  </tr>
  <tr>
    <th>19</th>
    <th>-0.267852</th>
    <th>0.159612</th>
    <th>-0.346919</th>
  </tr>
  <tr>
    <th>20</th>
    <th>-0.257258</th>
    <th>0.163018</th>
    <th>-0.344198</th>
  </tr>
  <tr>
    <th>21</th>
    <th>-0.242090</th>
    <th>0.159207</th>
    <th>-0.323443</th>
  </tr>
  <tr>
    <th>22</th>
    <th>-0.255733</th>
    <th>0.129341</th>
    <th>-0.322228</th>
  </tr>
  <tr>
    <th>23</th>
    <th>-0.235854</th>
    <th>0.143768</th>
    <th>-0.305106</th>
  </tr>
  <tr>
    <th>24</th>
    <th>-0.220397</th>
    <th>0.115682</th>
    <th>-0.289971</th>
  </tr>
  <tr>
    <th>25</th>
    <th>-0.233782</th>
    <th>0.135361</th>
    <th>-0.294088</th>
  </tr>
  <tr>
    <th>26</th>
    <th>-0.202050</th>
    <th>0.142435</th>
    <th>-0.279994</th>
  </tr>
  <tr>
    <th>27</th>
    <th>-0.196104</th>
    <th>0.119580</th>
    <th>-0.265333</th>
  </tr>
  <tr>
    <th>28</th>
    <th>-0.204124</th>
    <th>0.119595</th>
    <th>-0.266063</th>
  </tr>
  <tr>
    <th>29</th>
    <th>-0.204096</th>
    <th>0.131431</th>
    <th>-0.264097</th>
  </tr>
  <tr>
    <th>30</th>
    <th>-0.183655</th>
    <th>0.128817</th>
    <th>-0.254156</th>
  </tr>
</table>




![png](output_25_1.png)


#### 查看模型结果


```python
learn.gan_trainer.switch(gen_mode=True)
learn.show_results(ds_type=DatasetType.Train, rows=16, figsize=(8,8))
```


![png](output_27_0.png)

