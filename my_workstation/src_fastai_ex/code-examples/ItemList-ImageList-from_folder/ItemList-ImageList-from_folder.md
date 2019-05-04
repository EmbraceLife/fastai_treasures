

```python
from fastai.vision import *
```


```python
path_data = untar_data(URLs.MNIST_TINY); path_data.ls()
```




    [PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/valid'),
     PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/labels.csv'),
     PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/test'),
     PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/history.csv'),
     PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/models'),
     PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/train')]




```python
itemlist = ItemList.from_folder(path_data/'test')
itemlist
```




    ItemList (20 items)
    /Users/Natsume/.fastai/data/mnist_tiny/test/4605.png,/Users/Natsume/.fastai/data/mnist_tiny/test/617.png,/Users/Natsume/.fastai/data/mnist_tiny/test/205.png,/Users/Natsume/.fastai/data/mnist_tiny/test/6517.png,/Users/Natsume/.fastai/data/mnist_tiny/test/5988.png
    Path: /Users/Natsume/.fastai/data/mnist_tiny/test



How does such output above is generated?

behind the scenes, executing `itemlist` calls `ItemList.__repr__` which basically prints out `itemlist[0]` to `itemlist[4]`


```python
itemlist[0]
```




    PosixPath('/Users/Natsume/.fastai/data/mnist_tiny/test/4605.png')



and `itemlist[0]` basically calls `itemlist.get(0)` which returns `itemlist.items[0]`. That's why we have outputs like above.


```python
imagelist = ImageList.from_folder(path_data/'test')
imagelist
```




    ImageList (20 items)
    Image (3, 28, 28),Image (3, 28, 28),Image (3, 28, 28),Image (3, 28, 28),Image (3, 28, 28)
    Path: /Users/Natsume/.fastai/data/mnist_tiny/test



How does such output above is generated?

from `ItemList`, `ImageList` inherits `__repr__`. behind the scenes, executing `imagelist` calls `ImageList.__repr__` which basically prints out `imagelist[0]` to `imagelist[4]`


```python
imagelist[0]
```




![png](output_8_0.png)




```python
print(imagelist[0])
```

    Image (3, 28, 28)



```python
imagelist[0].__repr__()
```




    'Image (3, 28, 28)'



and `imagelist[0]` basically calls `imagelist.get(0)` which calls `imagelist.open(imagelist.items[0])` which returns `Image` object. This is why we see 'Image (3, 28, 28)' as output of `print(imagelist[0])`

the reason why we see printed out image as output of `imagelist[0]` is due to jupyter notebook's built-in functions.
