#AUTOGENERATED! DO NOT EDIT! File to edit: dev/10_layers.ipynb (unless otherwise specified).

__all__ = ['Lambda', 'PartialLayer', 'View', 'ResizeBatch', 'Flatten', 'Debugger', 'sigmoid_range', 'SigmoidRange',
           'PoolFlatten', 'AdaptiveConcatPool2d', 'NormType', 'BatchNorm', 'BatchNorm1dFlat', 'BnDropLin',
           'init_default', 'ConvLayer', 'FlattenedLoss', 'CrossEntropyLossFlat', 'BCEWithLogitsLossFlat', 'BCELossFlat',
           'MSELossFlat', 'trunc_normal_', 'Embedding', 'SelfAttention', 'PooledSelfAttention2d', 'icnr_init',
           'PixelShuffle_ICNR', 'SequentialEx', 'MergeLayer', 'SimpleCNN', 'ResBlock', 'ParameterModule',
           'children_and_parameters', 'TstModule', 'tst', 'children', 'flatten_model']

from .imports import *
from .test import *
from .core import *
from torch.nn.utils import weight_norm, spectral_norm

class Lambda(nn.Module):
    "An easy way to create a pytorch layer for a simple `func`"
    def __init__(self, func):
        super().__init__()
        self.func=func

    def forward(self, x): return self.func(x)
    def __repr__(self): return f'{self.__class__.__name__}({self.func})'

class PartialLayer(Lambda):
    "Layer that applies `partial(func, **kwargs)`"
    def __init__(self, func, **kwargs):
        super().__init__(partial(func, **kwargs))
        self.repr = f'{func.__name__}, {kwargs}'

    def forward(self, x): return self.func(x)
    def __repr__(self): return f'{self.__class__.__name__}({self.repr})'

class View(nn.Module):
    "Reshape `x` to `size`"
    def __init__(self, *size):
        super().__init__()
        self.size = size

    def forward(self, x): return x.view(self.size)

class ResizeBatch(nn.Module):
    "Reshape `x` to `size`, keeping batch dim the same size"
    def __init__(self, *size):
        super().__init__()
        self.size = size

    def forward(self, x):
        size = (x.size(0),) + self.size
        return x.view(size)

class Flatten(nn.Module):
    "Flatten `x` to a single dimension, often used at the end of a model. `full` for rank-1 tensor"
    def __init__(self, full=False):
        super().__init__()
        self.full = full

    def forward(self, x):
        return x.view(-1) if self.full else x.view(x.size(0), -1)

class Debugger(nn.Module):
    "A module to debug inside a model."
    def forward(self,x):
        set_trace()
        return x

def sigmoid_range(x, low, high):
    "Sigmoid function with range `(low, high)`"
    return torch.sigmoid(x) * (high - low) + low

class SigmoidRange(nn.Module):
    "Sigmoid module with range `(low, high)`"
    def __init__(self, low, high):
        super().__init__()
        self.low,self.high = low,high

    def forward(self, x): return sigmoid_range(x, self.low, self.high)

class PoolFlatten(nn.Sequential):
    "Combine `nn.AdaptiveAvgPool2d` and `Flatten`."
    def __init__(self): super().__init__(nn.AdaptiveAvgPool2d(1), Flatten())

class AdaptiveConcatPool2d(nn.Module):
    "Layer that concats `AdaptiveAvgPool2d` and `AdaptiveMaxPool2d`"
    def __init__(self, size=None):
        super().__init__()
        self.size = size or 1
        self.ap = nn.AdaptiveAvgPool2d(self.size)
        self.mp = nn.AdaptiveMaxPool2d(self.size)
    def forward(self, x): return torch.cat([self.mp(x), self.ap(x)], 1)

NormType = Enum('NormType', 'Batch BatchZero Weight Spectral')

def BatchNorm(nf, norm_type=NormType.Batch, ndim=2, **kwargs):
    "BatchNorm layer with `nf` features and `ndim` initialized depending on `norm_type`."
    assert 1 <= ndim <= 3
    bn = getattr(nn, f"BatchNorm{ndim}d")(nf, **kwargs)
    bn.bias.data.fill_(1e-3)
    bn.weight.data.fill_(0. if norm_type==NormType.BatchZero else 1.)
    return bn

class BatchNorm1dFlat(nn.BatchNorm1d):
    "`nn.BatchNorm1d`, but first flattens leading dimensions"
    def forward(self, x):
        if x.dim()==2: return super().forward(x)
        *f,l = x.shape
        x = x.contiguous().view(-1,l)
        return super().forward(x).view(*f,l)

class BnDropLin(nn.Sequential):
    "Module grouping `BatchNorm1d`, `Dropout` and `Linear` layers"
    def __init__(self, n_in, n_out, bn=True, p=0., act=None):
        layers = [BatchNorm(n_in, ndim=1)] if bn else []
        if p != 0: layers.append(nn.Dropout(p))
        layers.append(nn.Linear(n_in, n_out))
        if act is not None: layers.append(act)
        super().__init__(*layers)

def init_default(m, func=nn.init.kaiming_normal_):
    "Initialize `m` weights with `func` and set `bias` to 0."
    if func:
        if hasattr(m, 'weight'): func(m.weight)
        if hasattr(m, 'bias') and hasattr(m.bias, 'data'): m.bias.data.fill_(0.)
    return m

def _relu(inplace=False, leaky=None):
    "Return a relu activation, maybe `leaky` and `inplace`."
    return nn.LeakyReLU(inplace=inplace, negative_slope=leaky) if leaky is not None else nn.ReLU(inplace=inplace)

def _conv_func(ndim=2, transpose=False):
    "Return the proper conv `ndim` function, potentially `transposed`."
    assert 1 <= ndim <=3
    return getattr(nn, f'Conv{"Transpose" if transpose else ""}{ndim}d')

defaults.activation=nn.ReLU

class ConvLayer(nn.Sequential):
    "Create a sequence of convolutional (`ni` to `nf`), ReLU (if `use_activ`) and `norm_type` layers."
    def __init__(self, ni, nf, ks=3, stride=1, padding=None, bias=None, ndim=2, norm_type=NormType.Batch,
                 act_cls=defaults.activation, transpose=False, init=nn.init.kaiming_normal_, xtra=None):
        if padding is None: padding = ((ks-1)//2 if not transpose else 0)
        bn = norm_type in (NormType.Batch, NormType.BatchZero)
        if bias is None: bias = not bn
        conv_func = _conv_func(ndim, transpose=transpose)
        conv = init_default(conv_func(ni, nf, kernel_size=ks, bias=bias, stride=stride, padding=padding), init)
        if   norm_type==NormType.Weight:   conv = weight_norm(conv)
        elif norm_type==NormType.Spectral: conv = spectral_norm(conv)
        layers = [conv]
        if act_cls is not None: layers.append(act_cls())
        if bn: layers.append(BatchNorm(nf, norm_type=norm_type, ndim=ndim))
        if xtra: layers.append(xtra)
        super().__init__(*layers)

class FlattenedLoss():
    "Same as `loss_cls`, but flattens input and target."
    def __init__(self, loss_cls, *args, axis=-1, floatify=False, is_2d=True, **kwargs):
        self.func,self.axis,self.floatify,self.is_2d = loss_cls(*args,**kwargs),axis,floatify,is_2d
        functools.update_wrapper(self, self.func)

    def __repr__(self): return f"FlattenedLoss of {self.func}"
    @property
    def reduction(self): return self.func.reduction
    @reduction.setter
    def reduction(self, v): self.func.reduction = v

    def __call__(self, inp, targ, **kwargs):
        inp  = inp .transpose(self.axis,-1).contiguous()
        targ = targ.transpose(self.axis,-1).contiguous()
        if self.floatify and targ.dtype not in [torch.float16, torch.float32]: targ = targ.float()
        inp = inp.view(-1,inp.shape[-1]) if self.is_2d else inp.view(-1)
        return self.func.__call__(inp, targ.view(-1), **kwargs)

def CrossEntropyLossFlat(*args, axis=-1, **kwargs):
    "Same as `nn.CrossEntropyLoss`, but flattens input and target."
    return FlattenedLoss(nn.CrossEntropyLoss, *args, axis=axis, **kwargs)

def BCEWithLogitsLossFlat(*args, axis=-1, floatify=True, **kwargs):
    "Same as `nn.BCEWithLogitsLoss`, but flattens input and target."
    return FlattenedLoss(nn.BCEWithLogitsLoss, *args, axis=axis, floatify=floatify, is_2d=False, **kwargs)

def BCELossFlat(*args, axis=-1, floatify=True, **kwargs):
    "Same as `nn.BCELoss`, but flattens input and target."
    return FlattenedLoss(nn.BCELoss, *args, axis=axis, floatify=floatify, is_2d=False, **kwargs)

def MSELossFlat(*args, axis=-1, floatify=True, **kwargs):
    "Same as `nn.MSELoss`, but flattens input and target."
    return FlattenedLoss(nn.MSELoss, *args, axis=axis, floatify=floatify, is_2d=False, **kwargs)

def trunc_normal_(x, mean=0., std=1.):
    "Truncated normal initialization (approximation)"
    # From https://discuss.pytorch.org/t/implementing-truncated-normal-initializer/4778/12
    return x.normal_().fmod_(2).mul_(std).add_(mean)

class Embedding(nn.Embedding):
    "Embedding layer with truncated normal initialization"
    def __init__(self, ni, nf):
        super().__init__(ni, nf)
        trunc_normal_(self.weight.data, std=0.01)

class SelfAttention(nn.Module):
    "Self attention layer for `n_channels`."
    def __init__(self, n_channels):
        super().__init__()
        self.query = self._conv(n_channels, n_channels//8)
        self.key   = self._conv(n_channels, n_channels//8)
        self.value = self._conv(n_channels, n_channels)
        self.gamma = nn.Parameter(tensor([0.]))

    def _conv(self,n_in,n_out):
        return ConvLayer(n_in, n_out, ks=1, ndim=1, norm_type=NormType.Spectral, act_cls=None, bias=False)

    def forward(self, x):
        #Notation from the paper.
        size = x.size()
        x = x.view(*size[:2],-1)
        f,g,h = self.query(x),self.key(x),self.value(x)
        beta = F.softmax(torch.bmm(f.transpose(1,2), g), dim=1)
        o = self.gamma * torch.bmm(h, beta) + x
        return o.view(*size).contiguous()

class PooledSelfAttention2d(nn.Module):
    "Pooled self attention layer for 2d."
    def __init__(self, n_channels):
        super().__init__()
        self.n_channels = n_channels
        self.query = self._conv(n_channels, n_channels//8)
        self.key   = self._conv(n_channels, n_channels//8)
        self.value = self._conv(n_channels, n_channels//2)
        self.out   = self._conv(n_channels//2, n_channels)
        self.gamma = nn.Parameter(tensor([0.]))

    def _conv(self,n_in,n_out):
        return ConvLayer(n_in, n_out, ks=1, norm_type=NormType.Spectral, act_cls=None, bias=False)

    def forward(self, x):
        n_ftrs = x.shape[2]*x.shape[3]
        f = self.query(x).view(-1, self.n_channels//8, n_ftrs)
        g = F.max_pool2d(self.key(x),   [2,2]).view(-1, self.n_channels//8, n_ftrs//4)
        h = F.max_pool2d(self.value(x), [2,2]).view(-1, self.n_channels//2, n_ftrs//4)
        beta = F.softmax(torch.bmm(f.transpose(1, 2), g), -1)
        o = self.out(torch.bmm(h, beta.transpose(1,2)).view(-1, self.n_channels//2, x.shape[2], x.shape[3]))
        return self.gamma * o + x

def icnr_init(x, scale=2, init=nn.init.kaiming_normal_):
    "ICNR init of `x`, with `scale` and `init` function"
    ni,nf,h,w = x.shape
    ni2 = int(ni/(scale**2))
    k = init(x.new_zeros([ni2,nf,h,w])).transpose(0, 1)
    k = k.contiguous().view(ni2, nf, -1)
    k = k.repeat(1, 1, scale**2)
    k = k.contiguous().view([nf,ni,h,w]).transpose(0, 1)
    return k

class PixelShuffle_ICNR(nn.Sequential):
    "Upsample by `scale` from `ni` filters to `nf` (default `ni`), using `nn.PixelShuffle`."
    def __init__(self, ni, nf=None, scale=2, blur=False, norm_type=NormType.Weight, act_cls=defaults.activation):
        super().__init__()
        nf = ifnone(nf, ni)
        layers = [ConvLayer(ni, nf*(scale**2), ks=1, norm_type=norm_type, act_cls=act_cls, bias=False),
                  nn.PixelShuffle(scale)]
        layers[0][0].weight.data.copy_(icnr_init(layers[0][0].weight.data))
        if blur: layers += [nn.ReplicationPad2d((1,0,1,0)), nn.AvgPool2d(2, stride=1)]
        super().__init__(*layers)

class SequentialEx(nn.Module):
    "Like `nn.Sequential`, but with ModuleList semantics, and can access module input"
    def __init__(self, *layers):
        super().__init__()
        self.layers = nn.ModuleList(layers)

    def forward(self, x):
        res = x
        for l in self.layers:
            res.orig = x
            nres = l(res)
            # We have to remove res.orig to avoid hanging refs and therefore memory leaks
            res.orig = None
            res = nres
        return res

    def __getitem__(self,i): return self.layers[i]
    def append(self,l):      return self.layers.append(l)
    def extend(self,l):      return self.layers.extend(l)
    def insert(self,i,l):    return self.layers.insert(i,l)

class MergeLayer(nn.Module):
    "Merge a shortcut with the result of the module by adding them or concatenating them if `dense=True`."
    def __init__(self, dense:bool=False):
        super().__init__()
        self.dense=dense

    def forward(self, x): return torch.cat([x,x.orig], dim=1) if self.dense else (x+x.orig)

class SimpleCNN(nn.Sequential):
    "Create a simple CNN with `filters`."
    def __init__(self, filters, kernel_szs=None, strides=None, bn=True):
        nl = len(filters)-1
        kernel_szs = ifnone(kernel_szs, [3]*nl)
        strides    = ifnone(strides   , [2]*nl)
        layers = [ConvLayer(filters[i], filters[i+1], kernel_szs[i], stride=strides[i],
                  norm_type=(NormType.Batch if bn and i<nl-1 else None)) for i in range(nl)]
        layers.append(PoolFlatten())
        super().__init__(*layers)

class ResBlock(nn.Module):
    "Resnet block from `ni` to `nh` with `stride`"
    def __init__(self, expansion, ni, nh, stride=1, norm_type=NormType.Batch, **kwargs):
        super().__init__()
        norm2 = NormType.BatchZero if norm_type==NormType.Batch else norm_type
        nf,ni = nh*expansion,ni*expansion
        layers  = [ConvLayer(ni, nh, 3, stride=stride, norm_type=norm_type, **kwargs),
                   ConvLayer(nh, nf, 3, norm_type=norm2, act=None)
        ] if expansion == 1 else [
                   ConvLayer(ni, nh, 1, norm_type=norm_type, **kwargs),
                   ConvLayer(nh, nh, 3, stride=stride, norm_type=norm_type, **kwargs),
                   ConvLayer(nh, nf, 1, norm_type=norm2, act=None, **kwargs)
        ]
        self.convs = nn.Sequential(*layers)
        self.idconv = noop if ni==nf else ConvLayer(ni, nf, 1, act=None, **kwargs)
        self.pool = noop if stride==1 else nn.AvgPool2d(2, ceil_mode=True)

    def forward(self, x): return act_fn(self.convs(x) + self.idconv(self.pool(x)))

class ParameterModule(nn.Module):
    "Register a lone parameter `p` in a module."
    def __init__(self, p):
        super().__init__()
        self.val = p

    def forward(self, x): return x

def children_and_parameters(m):
    "Return the children of `m` and its direct parameters not registered in modules."
    children = list(m.children())
    children_p = sum([[id(p) for p in c.parameters()] for c in m.children()],[])
    for p in m.parameters():
        if id(p) not in children_p: children.append(ParameterModule(p))
    return children

class TstModule(nn.Module):
    def __init__(self):
        super().__init__()
        self.a = nn.Parameter(torch.randn(1))
        self.lin = nn.Linear(5,10)

tst = TstModule()
children = children_and_parameters(tst)
test_eq(len(children), 2)
test_eq(children[0], tst.lin)
assert isinstance(children[1], ParameterModule)
test_eq(children[1].val, tst.a)

def flatten_model(m):
    "Return the list of all submodules and parameters of `m`"
    return sum(map(flatten_model,children_and_parameters(m)),[]) if len(list(m.children())) else [m]