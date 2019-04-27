import fastai.vision as fv
import fastai.core as fc
# # %% markdown
# # typing
# # %%
# fc.AnnealFunc
# # %% markdown
# # %%
# fc.num_cpus()
#
# fc.Sizes
#
# fc.Tokens
#
# fc._default_cpus
#
# fc.defaults
#
# fc.SimpleNamespace
#
# fc.is_listy(2)
#
# fc.is_listy([2])
#
# fc.is_dict({'a':2})
#
# fc.is_pathlike(fc.Path('test'))
#
# fc.noop('string')
#
# a = fc.chunks(l=['a','b','c','d'], n=2)
#
# for i in a:
#     print(i)
#
#
# fc.to_int(b="2,3,4") # error
# fc.to_int(b="234")
# fc.to_int(b=["234",'23','12'])
# fc.to_int(b=("234",'23','12'))
# fc.to_int(b=("234",23,'12'))
# # %% markdown
# # %%
# fc.ifnone(a=1, b=2)
# fc.ifnone(a="yes", b=2)
# fc.ifnone(a=fc.np.array(1), b=2)
# fc.ifnone(a=None, b=2)
# fc.ifnone(a=None, b=None)
# # %% markdown
# # %%
# fc.is1d([1,2,3])
# fc.is1d(123)
# b = fc.np.array(([2,2],[3,4],[5,6]))
# fc.is1d(b)
# # %% markdown
# # %%
# c = fc.pd.array([9,2,1,8,5])
# fc.uniqueify(x=c)
# fc.uniqueify(x=c,sort=True)
# fc.uniqueify(x = [3,1,3,3,0])
# fc.uniqueify(x = [3,1,3,3,0], sort=True)
# fc.Series
# help(fc.Series)
# d = fc.Series([1,4,3,2,6])
# fc.uniqueify(x=d)
# # %% markdown
# # source code uniqueify
# # %%
# fc.OrderedDict.fromkeys(d)
# fc.OrderedDict.fromkeys(d).keys()
# list(fc.OrderedDict.fromkeys(d).keys())
# # %% markdown
# # %%
# fc.idx_dict([1,2,3])
# fc.idx_dict([23, 98, 100])
# # %% markdown
# # ## Explore ItemBase
# # __repr__
# # fc.plt.Axes how to use it?
#
# # %%
# ib = fc.ItemBase(data=1)
# ib.data
# ib.__class__
# ib.__class__.__name__
# ib.__repr__() # does not work for ItemBase, but on subclasses
# str(ib) # maximum recursion exceeded
# str(1)
# str(ib.data)
# # How to use ib.show
# fc.plt.Axes
# # %% markdown
# # %%
# el = fc.EmptyLabel()
# el.obj
# el # using ItemBase.__repr__(), it works
# el.__repr__()
# el.__str__() # subclass func
# el.__hash__() # subclass func
# el.data
# fc.ItemBase
# # %% markdown
# # %%
#

# path = fv.untar_data(fv.URLs.PETS);path
# fv.find_classes(folder=path)
#
#
fc.NPArrayMask
fc.NPArrayableList
fc.SplitArrayList
mask1=[1]
arr1 = [([1,2,3,4],[4,5,6,7]),([4,5,6,7],[4,5,6,7])]
fc.arrays_split(mask1, arr1)
fv.np.array([1,2,3,4])[fv.np.array(2)]
fv.np.array([1,2,3,4])[~fv.np.array(2)]
