
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Tabular-models" data-toc-modified-id="Tabular-models-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Tabular models</a></span><ul class="toc-item"><li><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#所需library" data-toc-modified-id="所需library-1.0.0.1"><span class="toc-item-num">1.0.0.1&nbsp;&nbsp;</span>所需library</a></span></li><li><span><a href="#pandas是必备" data-toc-modified-id="pandas是必备-1.0.0.2"><span class="toc-item-num">1.0.0.2&nbsp;&nbsp;</span>pandas是必备</a></span></li><li><span><a href="#下载数据" data-toc-modified-id="下载数据-1.0.0.3"><span class="toc-item-num">1.0.0.3&nbsp;&nbsp;</span>下载数据</a></span></li><li><span><a href="#预制-dep_var,-cat_names,-cont_names,-procs" data-toc-modified-id="预制-dep_var,-cat_names,-cont_names,-procs-1.0.0.4"><span class="toc-item-num">1.0.0.4&nbsp;&nbsp;</span>预制 <code>dep_var</code>, <code>cat_names</code>, <code>cont_names</code>, <code>procs</code></a></span></li><li><span><a href="#构建test-的data-source" data-toc-modified-id="构建test-的data-source-1.0.0.5"><span class="toc-item-num">1.0.0.5&nbsp;&nbsp;</span>构建test 的data source</a></span></li><li><span><a href="#在df和test-data-source基础上构建databunch" data-toc-modified-id="在df和test-data-source基础上构建databunch-1.0.0.6"><span class="toc-item-num">1.0.0.6&nbsp;&nbsp;</span>在df和test data source基础上构建databunch</a></span></li><li><span><a href="#展示10行batch数据样本" data-toc-modified-id="展示10行batch数据样本-1.0.0.7"><span class="toc-item-num">1.0.0.7&nbsp;&nbsp;</span>展示10行batch数据样本</a></span></li><li><span><a href="#构建tabular-learner模型" data-toc-modified-id="构建tabular-learner模型-1.0.0.8"><span class="toc-item-num">1.0.0.8&nbsp;&nbsp;</span>构建tabular learner模型</a></span></li><li><span><a href="#训练" data-toc-modified-id="训练-1.0.0.9"><span class="toc-item-num">1.0.0.9&nbsp;&nbsp;</span>训练</a></span></li></ul></li></ul></li><li><span><a href="#Inference" data-toc-modified-id="Inference-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Inference</a></span><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#如何做tabular-data预测" data-toc-modified-id="如何做tabular-data预测-1.1.0.1"><span class="toc-item-num">1.1.0.1&nbsp;&nbsp;</span>如何做tabular data预测</a></span></li></ul></li></ul></li></ul></li></ul></div>

# Tabular models

#### 所需library


```python
from fastai.tabular import *
```

#### pandas是必备

Tabular data should be in a Pandas `DataFrame`.

#### 下载数据


```python
path = untar_data(URLs.ADULT_SAMPLE)
df = pd.read_csv(path/'adult.csv')
```

#### 预制 `dep_var`, `cat_names`, `cont_names`, `procs`


```python
dep_var = 'salary'
cat_names = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race']
cont_names = ['age', 'fnlwgt', 'education-num']
procs = [FillMissing, Categorify, Normalize]
```

#### 构建test 的data source


```python
test = TabularList.from_df(df.iloc[800:1000].copy(), 
                           path=path, 
                           cat_names=cat_names, 
                           cont_names=cont_names)
```

#### 在df和test data source基础上构建databunch


```python
data = (TabularList.from_df(df, path=path, cat_names=cat_names, cont_names=cont_names, procs=procs)
                           .split_by_idx(list(range(800,1000)))
                           .label_from_df(cols=dep_var)
                           .add_test(test)
                           .databunch())
```

#### 展示10行batch数据样本


```python
data.show_batch(rows=10)
```


<table>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <col width='10%'>  <tr>
    <th>workclass</th>
    <th>education</th>
    <th>marital-status</th>
    <th>occupation</th>
    <th>relationship</th>
    <th>race</th>
    <th>education-num_na</th>
    <th>age</th>
    <th>fnlwgt</th>
    <th>education-num</th>
    <th>target</th>
  </tr>
  <tr>
    <th> Private</th>
    <th> HS-grad</th>
    <th> Never-married</th>
    <th> Sales</th>
    <th> Not-in-family</th>
    <th> White</th>
    <th>False</th>
    <th>-1.2158</th>
    <th>1.1004</th>
    <th>-0.4224</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> ?</th>
    <th> HS-grad</th>
    <th> Widowed</th>
    <th> ?</th>
    <th> Not-in-family</th>
    <th> White</th>
    <th>False</th>
    <th>1.8627</th>
    <th>0.0976</th>
    <th>-0.4224</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> Self-emp-not-inc</th>
    <th> HS-grad</th>
    <th> Never-married</th>
    <th> Craft-repair</th>
    <th> Own-child</th>
    <th> Black</th>
    <th>False</th>
    <th>0.0303</th>
    <th>0.2092</th>
    <th>-0.4224</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> Private</th>
    <th> HS-grad</th>
    <th> Married-civ-spouse</th>
    <th> Protective-serv</th>
    <th> Husband</th>
    <th> White</th>
    <th>False</th>
    <th>1.5695</th>
    <th>-0.5938</th>
    <th>-0.4224</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> Private</th>
    <th> HS-grad</th>
    <th> Married-civ-spouse</th>
    <th> Handlers-cleaners</th>
    <th> Husband</th>
    <th> White</th>
    <th>False</th>
    <th>-0.9959</th>
    <th>-0.0318</th>
    <th>-0.4224</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> Private</th>
    <th> 10th</th>
    <th> Married-civ-spouse</th>
    <th> Farming-fishing</th>
    <th> Wife</th>
    <th> White</th>
    <th>False</th>
    <th>-0.7027</th>
    <th>0.6071</th>
    <th>-1.5958</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> Private</th>
    <th> HS-grad</th>
    <th> Married-civ-spouse</th>
    <th> Machine-op-inspct</th>
    <th> Husband</th>
    <th> White</th>
    <th>False</th>
    <th>0.1036</th>
    <th>-0.0968</th>
    <th>-0.4224</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> Private</th>
    <th> Some-college</th>
    <th> Married-civ-spouse</th>
    <th> Exec-managerial</th>
    <th> Own-child</th>
    <th> White</th>
    <th>False</th>
    <th>-0.7760</th>
    <th>-0.6653</th>
    <th>-0.0312</th>
    <th>>=50k</th>
  </tr>
  <tr>
    <th> State-gov</th>
    <th> Some-college</th>
    <th> Never-married</th>
    <th> Tech-support</th>
    <th> Own-child</th>
    <th> White</th>
    <th>False</th>
    <th>-0.8493</th>
    <th>-1.4959</th>
    <th>-0.0312</th>
    <th><50k</th>
  </tr>
  <tr>
    <th> Private</th>
    <th> 11th</th>
    <th> Never-married</th>
    <th> Machine-op-inspct</th>
    <th> Not-in-family</th>
    <th> White</th>
    <th>False</th>
    <th>-1.0692</th>
    <th>-0.9516</th>
    <th>-1.2046</th>
    <th><50k</th>
  </tr>
</table>



#### 构建tabular learner模型


```python
learn = tabular_learner(data, layers=[200,100], metrics=accuracy)
```

#### 训练


```python
learn.fit(1, 1e-2)
```


Total time: 00:03 <p><table style='width:300px; margin-bottom:10px'>
  <tr>
    <th>epoch</th>
    <th>train_loss</th>
    <th>valid_loss</th>
    <th>accuracy</th>
  </tr>
  <tr>
    <th>1</th>
    <th>0.354604</th>
    <th>0.378520</th>
    <th>0.820000</th>
  </tr>
</table>



## Inference

#### 如何做tabular data预测


```python
row = df.iloc[0]
```


```python
learn.predict(row)
```




    (Category >=50k, tensor(1), tensor([0.4402, 0.5598]))


