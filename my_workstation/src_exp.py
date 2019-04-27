# %%markdown
# # fastai/core.py
import fastai.core as fc
fc.ifnone
fc.num_cpus()

fc.Sizes

fc.Tokens

fc._default_cpus

fc.defaults

fc.SimpleNamespace

fc.is_listy(2)

fc.is_listy([2])

fc.is_dict({'a':2})

fc.is_pathlike(fc.Path('test'))

fc.noop('string')

a = fc.chunks(l=['a','b','c','d'], n=2)

for i in a:
    print(i)


fc.to_int(b="2,3,4") # error
fc.to_int(b="234")
fc.to_int(b=["234",'23','12'])
fc.to_int(b=("234",'23','12'))
fc.to_int(b=("234",23,'12'))

fc.ifnone(a=1, b=2)
fc.ifnone(a="yes", b=2)
fc.ifnone(a=fc.np.array(1), b=2)
fc.ifnone(a=None, b=2)
fc.ifnone(a=None, b=None)

fc.is1d([1,2,3])
fc.is1d(123)
b = fc.np.array(([2,2],[3,4],[5,6]))
fc.is1d(b)
