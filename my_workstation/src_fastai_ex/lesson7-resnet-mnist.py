# %% markdown
# ## MNIST CNN
# %%
# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline
# %%
import fastai.vision as fv
from fastai.vision import *

# %% markdown
# ### Data
# %%
path = untar_data(URLs.MNIST)

# %%
path.ls()
# %%
il = ImageList.from_folder(path, convert_mode='L')
il_test = ImageList.from_folder(path, convert_mode='L', include='testing')
# %%
il.items[0]
# %%
defaults.cmap='binary'
# %%
il
# %%
il[0].show()
# %%
sd = il.split_by_folder(train='training', valid='testing')
# %%
sd
# %%
(path/'training').ls()
# %%
ll = sd.label_from_folder()
# %%
ll
# %%
x,y = ll.train[0]
# %%
x.show()
print(y,x.shape)
# %%
tfms = ([*rand_pad(padding=3, size=28, mode='zeros')], [])
# %%
ll = ll.transform(tfms)
# %%
bs = 128
# %%
# not using imagenet_stats because not using pretrained model
data = ll.databunch(bs=bs).normalize()
# %%
x,y = data.train_ds[0]
# %%
x.show()
print(y)
# %%
def _plot(i,j,ax): data.train_ds[0][0].show(ax, cmap='gray')
plot_multi(_plot, 3, 3, figsize=(8,8))
# %%
xb,yb = data.one_batch()
xb.shape,yb.shape
# %%
data.show_batch(rows=3, figsize=(5,5))
# %% markdown
# ### Basic CNN with batchnorm
# %%
def conv(ni,nf): return nn.Conv2d(ni, nf, kernel_size=3, stride=2, padding=1)
# %%
model = nn.Sequential(
    conv(1, 8), # 14
    nn.BatchNorm2d(8),
    nn.ReLU(),
    conv(8, 16), # 7
    nn.BatchNorm2d(16),
    nn.ReLU(),
    conv(16, 32), # 4
    nn.BatchNorm2d(32),
    nn.ReLU(),
    conv(32, 16), # 2
    nn.BatchNorm2d(16),
    nn.ReLU(),
    conv(16, 10), # 1
    nn.BatchNorm2d(10),
    Flatten()     # remove (1,1) grid
)
# %%
learn = Learner(data, model, loss_func = nn.CrossEntropyLoss(), metrics=accuracy)
# %%
print(learn.summary())
# %%
xb = xb.cuda()
# %%
model(xb).shape
# %%
learn.lr_find(end_lr=100)
# %%
learn.recorder.plot()
# %%
learn.fit_one_cycle(3, max_lr=0.1)
# %% markdown
# ### Refactor
# %%
def conv2(ni,nf): return conv_layer(ni,nf,stride=2)
# %%
model = nn.Sequential(
    conv2(1, 8),   # 14
    conv2(8, 16),  # 7
    conv2(16, 32), # 4
    conv2(32, 16), # 2
    conv2(16, 10), # 1
    Flatten()      # remove (1,1) grid
)
# %%
learn = Learner(data, model, loss_func = nn.CrossEntropyLoss(), metrics=accuracy)
# %%
learn.fit_one_cycle(10, max_lr=0.1)
# %% markdown
# ### Resnet-ish
# %%
class ResBlock(nn.Module):
    def __init__(self, nf):
        super().__init__()
        self.conv1 = conv_layer(nf,nf)
        self.conv2 = conv_layer(nf,nf)

    def forward(self, x): return x + self.conv2(self.conv1(x))
# %%
help(res_block)
# %%
model = nn.Sequential(
    conv2(1, 8),
    res_block(8),
    conv2(8, 16),
    res_block(16),
    conv2(16, 32),
    res_block(32),
    conv2(32, 16),
    res_block(16),
    conv2(16, 10),
    Flatten()
)
# %%
def conv_and_res(ni,nf): return nn.Sequential(conv2(ni, nf), res_block(nf))
# %%
model = nn.Sequential(
    conv_and_res(1, 8),
    conv_and_res(8, 16),
    conv_and_res(16, 32),
    conv_and_res(32, 16),
    conv2(16, 10),
    Flatten()
)
# %%
learn = Learner(data, model, loss_func = nn.CrossEntropyLoss(), metrics=accuracy)
# %%
learn.lr_find(end_lr=100)
learn.recorder.plot()
# %%
learn.fit_one_cycle(12, max_lr=0.05)
# %%
print(learn.summary())
# %% markdown
# ## fin
# %%
