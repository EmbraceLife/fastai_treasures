# fastai courses inside out
[my translation contribution](https://www.youtube.com/timedtext_cs_panel?o=U&ar=2)
[my video manager](https://www.youtube.com/my_videos?o=U&ar=2)
[lesson1](https://youtu.be/NO-HCRg9VKw)
[lesson2](https://youtu.be/wkyvJQSOW_Q)



## Why? -> Jeremy's advice
writing/teaching notebook from scratch == qualified to be a top practitioner

## How? -> Break and conquer + iterate
- codes
- key points
- videos
- iterate
- to re-teach the course in English and Chinese

## Do it together
- read and translate the English subtitles into Chinese
- ask and discuss your uncertainties





- Lesson 7 will be intensive 节奏紧张 [0:00:06](https://youtu.be/9spwoDYwW_I?t=6)
- food classifer app 食物识别器APP [0:01:04](https://youtu.be/9spwoDYwW_I?t=64)
- Notebook start 讲解开始 [0:02:08](https://youtu.be/9spwoDYwW_I?t=128)
- Purpose: CNN scratch 目标：手动构建CNN [0:02:17](https://youtu.be/9spwoDYwW_I?t=137)
- Specify the meaning of implementing from scratch 手动构建的意思 [0:02:33](https://youtu.be/9spwoDYwW_I?t=153)
- use full MNIST 采用全部MNIST数据集 [0:02:41](https://youtu.be/9spwoDYwW_I?t=161)
- Viewing MNIST subfolders 查看MNIST子文件夹 [0:02:52](https://youtu.be/9spwoDYwW_I?t=172)
- Purpose: data block API one at a time 逐一使用data block api [0:02:59](https://youtu.be/9spwoDYwW_I?t=179)
- Touch on ImageList 点到ImageList [0:03:12](https://youtu.be/9spwoDYwW_I?t=192)
- ImageList.from_folder 从文件夹提供图片 [0:03:19](https://youtu.be/9spwoDYwW_I?t=199)
- Use of PIL and its convert_mode 图片打开方式 [0:03:27](https://youtu.be/9spwoDYwW_I?t=207)
- Understanding ItemList.items 理解 ItemList.items [0:03:53](https://youtu.be/9spwoDYwW_I?t=233)
- understanding defaults.cmap 理解 defaults.cmap [0:04:12](https://youtu.be/9spwoDYwW_I?t=252)
- 1 channel image as rank 3 tensor [0:04:36](https://youtu.be/9spwoDYwW_I?t=276)
- why not matrix but rank 3 tensor [0:04:53](https://youtu.be/9spwoDYwW_I?t=293)
- understanding `.items` 理解 `.items` [0:05:11](https://youtu.be/9spwoDYwW_I?t=311)
- understanding `ImageList[0].show()` [0:05:18](https://youtu.be/9spwoDYwW_I?t=318)
- understanding `il.split_by_folder`, `il.no_split` [0:05:29](https://youtu.be/9spwoDYwW_I?t=329)
- dataset split work procedures [0:05:48](https://youtu.be/9spwoDYwW_I?t=348)
- distinguish training, validation, testing set 如何区分训练，验证，测试集[0:05:56](https://youtu.be/9spwoDYwW_I?t=356)
- use `test=` to do inference [0:06:37](https://youtu.be/9spwoDYwW_I?t=397)
- when to `label_from_folder` [0:06:54](https://youtu.be/9spwoDYwW_I?t=414)
- take a training sample to see label and image [0:07:28](https://youtu.be/9spwoDYwW_I?t=448)
- when and how to add transforms with free style [0:07:55](https://youtu.be/9spwoDYwW_I?t=475)
    - `*rand_pad`, `[]` for validation set, `.transform(tfms)`
- how to set `.normalize` when not using pretrained model [0:08:47](https://youtu.be/9spwoDYwW_I?t=527)
- viewing transform effect with `plot_multi`, `_plot` [0:09:22](https://youtu.be/9spwoDYwW_I?t=562)
- 从LL到DataBunch，图片被加入了形变，批量和normalization
- 因为是随机padding,每次变形都不太一样
- how to get `data.one_batch()` and `show_batch()` sensibly [0:10:27](https://youtu.be/9spwoDYwW_I?t=627)
- why to refactor conv_layer with same params [0:11:01](https://youtu.be/9spwoDYwW_I?t=661)
- how to create the first conv_layer of the convnet [0:11:35](https://youtu.be/9spwoDYwW_I?t=695)
- how to build the rest of convnet with stride, channel choices [0:12:41](https://youtu.be/9spwoDYwW_I?t=761)
- why and how to `Flatten` a rank 3 tensor to a vector [0:13:18](https://youtu.be/9spwoDYwW_I?t=798)
- how to create and interpret `learn.summary()` [0:14:09](https://youtu.be/9spwoDYwW_I?t=849)
- how to do prediction on a batch [0:14:49](https://youtu.be/9spwoDYwW_I?t=889)
- simple training steps [0:15:17](https://youtu.be/9spwoDYwW_I?t=917)
- a little refactor on creating a convnet [0:15:42](https://youtu.be/9spwoDYwW_I?t=942)
- train over a minute after refactor [0:16:11](https://youtu.be/9spwoDYwW_I?t=971)
- how to improve neuralnet by making it deeper [0:16:23](https://youtu.be/9spwoDYwW_I?t=983)
- what is the problem with deeper neuralnet without batch norm [0:16:47](https://youtu.be/9spwoDYwW_I?t=1007)
- how good researcher react to weird things [0:17:55](https://youtu.be/9spwoDYwW_I?t=1075)
- how Kaiming He approached the problem [0:18:04](https://youtu.be/9spwoDYwW_I?t=1084)
- what is the skip connection solution [0:18:27](https://youtu.be/9spwoDYwW_I?t=1107)
- summarize the intuition behind skip connection [0:19:51](https://youtu.be/9spwoDYwW_I?t=1191)
- why Res-block is revolutionary [0:20:09](https://youtu.be/9spwoDYwW_I?t=1209)
- Why exactly Res-block is so powerful from a recent neurIPS paper [0:21:16](https://youtu.be/9spwoDYwW_I?t=1276)
- How to create a res_block from scratch [0:22:56](https://youtu.be/9spwoDYwW_I?t=1376)
- How to use `res_block` of fastai [0:23:31](https://youtu.be/9spwoDYwW_I?t=1411)
- How to embed res_blocks into the previous CNN [0:23:50](https://youtu.be/9spwoDYwW_I?t=1430)
- How to further refactor to make Resnet-ish architecture [0:24:10](https://youtu.be/9spwoDYwW_I?t=1450)
- Why refactor makes you a better researcher [0:24:25](https://youtu.be/9spwoDYwW_I?t=1465)
- How powerful Resnet is [0:25:04](https://youtu.be/9spwoDYwW_I?t=1504)
- popularity makes it highly optimized than other new achitectures [0:25:57](https://youtu.be/9spwoDYwW_I?t=1557)
- How res_block is constructed in fastai resemble and differ from our hand-made res_block [0:26:16](https://youtu.be/9spwoDYwW_I?t=1576)
- What is MergeLayer [0:26:27](https://youtu.be/9spwoDYwW_I?t=1587)
- What is `x.orig` and `SequentialEx` [0:26:43](https://youtu.be/9spwoDYwW_I?t=1603)
- What is dense block or dense net [0:27:19](https://youtu.be/9spwoDYwW_I?t=1639)
- How does dense net work? [0:28:16](https://youtu.be/9spwoDYwW_I?t=1696)
- What are pros and cons of dense net? [0:28:56](https://youtu.be/9spwoDYwW_I?t=1736)
- Resnet's skip connection use for segmentation [0:30:19](https://youtu.be/9spwoDYwW_I?t=1819)
- Unet is great on segmentation and we are about to understand how it work [0:30:51](https://youtu.be/9spwoDYwW_I?t=1851)
- How does segmentation work and what is the challenge [:0:31:56](https://youtu.be/9spwoDYwW_I?t=1916)
- Unet on segmentation: how to do downsampling [0:33:17](https://youtu.be/9spwoDYwW_I?t=1997)
- deconvolution to get upsampling feature map [0:35:28](https://youtu.be/9spwoDYwW_I?t=2128)
- pros and cons of earlier version of deconvolution [0:36:10](https://youtu.be/9spwoDYwW_I?t=2170)
- new approach 1: nearest neighbor interpolation [0:38:21](https://youtu.be/9spwoDYwW_I?t=2301)
- new approach 2: bilinear interpolation [0:39:40](https://youtu.be/9spwoDYwW_I?t=2380)
- new approach 3: pixel shuffle [0:40:34](https://youtu.be/9spwoDYwW_I?t=2434)
- basic idea and challenge of upsampling [0:40:48](https://youtu.be/9spwoDYwW_I?t=2448)
- Unet paper: how it resolve upsampling challenges with larger skip connection [0:41:44](https://youtu.be/9spwoDYwW_I?t=2504)
- Understanding Unet source code: what is encoder [0:43:33](https://youtu.be/9spwoDYwW_I?t=2613)
- Understanding Unet source code: what is middle_conv [0:44:11](https://youtu.be/9spwoDYwW_I?t=2651)
- Understanding Unet source code: what is `sfs_idxs` [0:44:41](https://youtu.be/9spwoDYwW_I?t=2681)
- Understanding Unet source code: cross connection and many other tricks [0:44:59](https://youtu.be/9spwoDYwW_I?t=2699)
- Understanding Unet source code: hooks get activations from downsampling path [0:45:55](https://youtu.be/9spwoDYwW_I?t=2755)
- alwasy replace two convs in a row with res_block [0:46:47](https://youtu.be/9spwoDYwW_I?t=2807)
- How Unet got attention [0:47:11](https://youtu.be/9spwoDYwW_I?t=2831)
- another use for Unet: what is image generation including restoration [0:48:24](https://youtu.be/9spwoDYwW_I?t=2904)
- Q&A: why concat before not after conv2(conv1(x)) [0:49:46](https://youtu.be/9spwoDYwW_I?t=2986)
- Q&A: How concat of densenet work with changing feature map sizes [0:50:53](https://youtu.be/9spwoDYwW_I?t=3053)
- image restoration: crappification logic, source code and be creative [0:52:02](https://youtu.be/9spwoDYwW_I?t=3122)
- create and train a model to turn crappy images to good ones [0:55:08](https://youtu.be/9spwoDYwW_I?t=3308)
  - why to use a pretrained model for image restoration? [0:55:44](https://youtu.be/9spwoDYwW_I?t=3344)
- Why the upsampling task is challenging? [0:58:26](https://youtu.be/9spwoDYwW_I?t=3506)
- How does GAN help with upsampling [0:59:21](https://youtu.be/9spwoDYwW_I?t=3561)
- How to understand the use of critic [1:00:17](https://youtu.be/9spwoDYwW_I?t=3617)
- How does GAN work [1:01:47](https://youtu.be/9spwoDYwW_I?t=3707)
- fastai version of GAN: the pain of training mainstream GANs [1:02:49](https://youtu.be/9spwoDYwW_I?t=3769)
- How does fastai GAN work: getting the pretrained generator and critic, how to get gen_images and original images folders, writing your own codes, gc.collect, [1:03:50](https://youtu.be/9spwoDYwW_I?t=3830)
- How does fastai GAN work: to create the critic [1:04:04](https://youtu.be/9spwoDYwW_I?t=3844)
- writing your own code with fastai library [1:05:28](https://youtu.be/9spwoDYwW_I?t=3928)
- the use of gc.collect [1:06:11](https://youtu.be/9spwoDYwW_I?t=3971)
- how to create a critic [1:06:55](https://youtu.be/9spwoDYwW_I?t=4015)
-
