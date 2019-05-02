#!/usr/bin/env python
# coding: utf-8

# We can get a little glimpse of how `ItemList`'s basic attributes and methods behave with the following code examples.

# In[48]:


import fastai.vision as fv


# In[49]:


path_data = fv.untar_data(fv.URLs.MNIST_TINY)


# In[50]:


il_data = fv.ItemList.from_folder(path_data, extensions=['.csv'])


# When executing `il_data`, it is `il_data.__repr__()` working under the hood. (when `ItemList.__repr__` is not available, `built_in` function `repr(il_data)` will work instead.)

# In[52]:


il_data


# In[51]:


il_data.__repr__()


# In[53]:


repr(il_data)


# Here is how to access the path of `ItemList` and the actual files or `items` in the path.

# In[54]:


il_data.path


# In[55]:


il_data.items


# `len(il_data)` is equivalent to and made possible by `il_data.__len__()`.

# In[56]:


len(il_data)


# In[57]:


il_data.__len__()


# `il_data[idx]` is equivalent to and made possible by `il_data.__getitem__(idx)`, which uses `il_data.get(idx)`. (But for `il_data.get(idx)`, `idx` has to be integer.)

# In[58]:


il_data.__getitem__(1.0)


# In[59]:


il_data[1.0]


# In[60]:


il_data.get(1)


# With `ItemList.new` we can make a copy with different reference.

# In[61]:


il_data_new = il_data.new(il_data.items); il_data_new


# In[62]:


hash(il_data)


# In[63]:


hash(il_data_new)


# In[64]:


il_data == il_data_new


# With `ItemList.add` we can concatenate two ItemLists together

# In[65]:


il_data.add(il_data_new)


# In[ ]:




