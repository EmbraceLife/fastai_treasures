## Lesson 7 Resnet, U-net, GAN


[details="本课预览"]
### A warning of lesson 7 and a student role model to checkout
[A warning of lesson 7 and a student role model to checkout](https://ytcropper.com/cropped/DG5c64cfb94e359)
0：00-1:59
	- Food classifier with fastai on Android and IOS app 
	- help docs, tutorials, community organizing 
[/details]
[details="如何一步一步链接data block"]

### How to do `data block` api step by step?
1:59-11:02
[How to do `data block` api step by step](https://ytcropper.com/cropped/DG5c64dec1a5040)
	- how to extract images with gray scale with `ImageItemList.from_folder` and `convert_mode`?
	- how to access each item from the folder path object?
	- how to set the default color map for fastai?
	- why fastai make each image into a rank 3 tensor rather than a 2D matrix?
	- how to access an image item as file path and item as image?
	- how to split training and validation sets by two folders “training” and “testing”?
		- the images inside “testing” folder do has labels, not real testing data without label
	- How to check what included inside training set folder?
		- inside training set folder, there is a folder for each class
	- how to provide labels for your training and validation sets?
		- then check to see the difference from previous step
	- how to access a single image example from training set with both x and y?
	- how to do transforms for small image dataset recognition?
		- how to do it with tuple setting for transforms?
	- how to create `DataBunch` with `normalize`?
	- how to access data example from `DataBunch.train_ds`?
	- how to plot an image from `data.train_ds`? 
		- how to plot this image with different transformations?
	- how to get a batch of x and y from `DataBunch`?
	- how to show a batch of data?
[/details]
[details="如何手写CNN"]

### How to create a CNN model from scratch
[How to create a CNN model from scratch](https://ytcropper.com/cropped/DG5c61eb74549f3)
11:00-16:54
	- How to refactor `nn.Conv2d` for usual use?
		- leaving two function inputs:
			- `ni`: number of input channels
			- `nf`: number of output channels 
			- `#14` : the size of feature map `14 x 14`
	- How down-sampling from `7x7` to `4x4`?
		- 7/2=3.5 + `max_ceiling` = 4
	- How to build a CNN model with `conv` and `BatchNorm2d` and `Relu`?
		- [image:16EDA985-0D1A-4765-A638-A584274C1AFD-76996-00031B1524A7B3E7/31DEDE98-8C85-49DD-8BBD-805C7617B89C.png]
	- How to use a single batch of data `xb` to double check on `model` built above?
		- [image:30C46125-9967-4C3A-8CA4-E4D671AF1DBD-76996-00031BCD20A29908/E30127C3-CE26-42E0-AF31-531AF1DC1C19.png]

	- How to refactor code further into `conv2`?
		- use fastai `conv_layer` which include `conv2d`, `BatchNorm` and `Relu`
		- refactor `conv_layer` into `conv2` with `stride=2`
[/details]
[details="如何手写Resnet"]

### How to create a Resnet from scratch
16:10-31:02
[How to create a Resnet from scratch](https://ytcropper.com/cropped/DG5c61ef6112786)
How to make the CNN deeper without shrink feature map size?
what caused a deeper CNN model to perform worse than a shallow one?
	- [image:07F9441D-7B1B-42C7-AB03-511415A802C2-76996-00030C8FB1006D28/5F24E25C-4439-4077-BDE9-1F48D0CF7A30.png]
what does really good researcher do in front this kind of problem?
What is the key insight that ResNet or ResNet block offers to us? (identity/skip connection)
What the real reason for why ResNet block work so well?
	- [image:4291DC80-8849-40B6-B0BA-EA852DFAB7F2-76996-00030CDE88DA86CA/CC14544A-4771-453E-B8CA-7A32D0B5DCD2.png]
How to write the ResNet block?
	- [image:5FD3BB7A-9C45-44C5-9C19-339F57D213DC-76996-00030CEA99BEF92C/2D3B65A4-D464-4B14-BA1D-1259E04C3094.png]
How to build the ResNet model?
	- [image:AB5244DF-26E5-4ED5-9868-41E9D041F6C6-76996-00030CFD98B63574/25A2D232-5166-4BF7-87D9-4003793E359F.png]
[/details]
[details="如何创建Resnet block和Dense block"]

#### ::How to use `sequentialEx` and `mergeLayer` to create `Resnet block` and `Dense block`?::
26:18-31:36
[How to use `sequentialEx` and `mergeLayer` to create `Resnet block` and `Dense block`](https://ytcropper.com/cropped/DG5c6499bd0bfa5)
What are the pros and cons of Dense net?
What kind of tasks or problems does Dense net good at solving?
How does it link to U-net?
[/details]
[details="如何手动创建U-net"]

### How to build upgraded U-net from scratch?
29:50-48:38
[How to build upgraded U-net from scratch](https://ytcropper.com/cropped/DG5c6201712f98d)
	- [how much better skip/dense connection help to strengthen U-net on segmentation?](https://ytcropper.com/cropped/DG5c649bce1b9eb)
		- 29:50-32:12
	- [What does it mean by upgrading U-net with ResNet and Deconvolution](https://ytcropper.com/cropped/DG5c649d68af7bf)
		- 32:00-36:10	
	* [What is the wasteful way of doing deconvolution and what is the better way (nearest neighbor interpolation?](https://ytcropper.com/cropped/DG5c649f69b1636)
		* 36:08-41:20
		* how to enlarge feature maps not shrink anymore?
		* [image:59E5FB01-2CFB-47DA-8085-05DD1DE7368D-76996-00031687B20EFB04/71B721CF-5FD1-494C-86BD-6149546E7D33.png]
		* part2 : pixel shuffle > NN interpolation
	- [How to implement U-net?](https://ytcropper.com/cropped/DG5c64a27e7e9c5)
		- 41:20-48:31
		- why simple convolution (down-sampling) + deconvolution(up-sampling) won’t work
		- What kind of special skip connection does U-net have?
			- skip long distance and not add but concat 
		- [How such special skip connection enable U-net to better segmentation?](https://ytcropper.com/cropped/DG5c64a46bef560)
			- 41:20-43:35
		- [What is the U-net implementation?](https://ytcropper.com/cropped/DG5c64a5f6539b3)
			- 43:30-47:24
			- what does a UnetBlock do and how to implement it?
		- How exactly does U-net train? ::Not explained in the course::
[/details]
[details="问答：为什么要在之前做concat，以及如何用dense concat防止缩水"]

### QA Why concat before and How to keep dense concat without shrinking
49:50-52:02
[Why concat before and How to keep dense concat without shrinking](https://youtu.be/DGdRC4h78_o)
[/details]



[details="如何将低像素图片还原成高像素图片"]
## How to make low resolution image with high resolution image
48:29-97:13
[How to make low resolution image with high resolution image](https://ytcropper.com/cropped/DG5c62186d95797)

[/details]
[details="什么是图片还原"]
### What is image restoration?
48:29-49:50
[What is image restoration](https://ytcropper.com/cropped/DG5c63393c5a833)
What are those specific applications of image restoration?
[/details]
[details="如何将原图变像素很差图"]

### How to crappify image as low resolution?
52:04-55:12
[How to crappify image as low resolution](https://ytcropper.com/cropped/DG5c633ce555d99)
Why to crappify image?
How did Jeremy do it? (low res and text written)
	* How to open image file
	* How to resize and bilinear interpolation
	* How to write a text on the image
	* How to save image with random quality level
[image:729A7FED-5489-478E-9D46-D06A95DE02D3-76996-0002E3F330FC7744/F7BF4E6B-D36E-4081-8005-6884400B0C9E.png]
Why not always see the text or number?
[image:16DA9837-D19A-4F7B-8796-EE82F3B0FC08-76996-0002E3F80F200E0C/685F50BB-D57C-4F3E-84A9-8BEDC654C340.png]
How to speed up with parallel?
[image:28BC542D-07E2-4ACA-82DD-26C52FFE4FE4-76996-0002E45B5374B1E2/A4868BD2-6333-44FC-B583-AE07FFF2666C.png]
How to come with your own crappification?
	- this is how to make something interesting or original
Why crappify is important to models to learn?
[/details]
[details="如何训练模型来消除水印"]

### How to train a model to remove watermarks
55:12-58:11
[How to train a model to remove watermarks](https://ytcropper.com/cropped/DG5c6350c25d93e)
Why use a U-net to train?
How to create the DataBunch?
Why need transfer learning to get rid of the text in the image?
What is a generator learner?
What does `MSELossFlat`do here?
What is frozen for the U-net?
[image:846764AE-B33B-4504-8F95-CE6412299973-76996-0002E6F8C0878DB5/FDC2EBA7-29CB-4C0D-94EB-E39596FA4DCB.png]
[/details]
[details="如何用GAN来提升图片像素"]

### How to use GAN to upgrade image resolution?
58:10-64:07
[How to use GAN to upgrade image resolution](https://ytcropper.com/cropped/DG5c636e343691e)
why to blame the MSE loss for current model can’t upgrade the resolution?
How GAN solves the upgrade problem with another loss function by calling another model?
How to understand all the concepts and the workflow in the diagram below?
[image:D3D36EFF-991E-4A7B-934C-276869A877A0-76996-0002F142639FB908/8E89A71B-A3FB-462A-8A96-279CC9BB7A7C.png](how loss change between different stages)
How the generator training and critic training do the ping pong game?
why it is a pain to train GAN (very slow to train especially at the beginning)?
How can pretrained both generator and discriminator to solve this problem?
[/details]
[details="如何构建和训练discriminator来区分真假图"]

### How to build and train a discriminator to tell `images` and `image_gen`
64:07-70:10
[How to build and train a discriminator to tell `images` and `image_gen`](https://ytcropper.com/cropped/DG5c63a0d68e33d)
What folders of images do we need for discriminator training?
How to generate and save prediction images into a folder?
	- how to create and remove directories (trees)
	- how to get all the image file names
	- how to access each batch of files at a time
	- how to save images with specific names in a directory
	- [image:EDA6CF1C-83E8-4351-A8FF-0F144B9431B5-76996-0002F6B41F32AE5B/7A5230C9-302E-4B45-9DEC-8FE5394AAAA1.png]

Why we should start to learn write our own codes/functions?
How to use GPU memory efficiently to avoid restarting notebook?
How create `DataBunch` for discriminator with two classes `images` and `image_gen`?
	- [image:ECD5A2F8-A1D2-4CF7-8A89-9C3495D82150-76996-0002F6AC6B981613/381EAF2C-0163-4BF1-9B31-744143C9E2D5.png]
Why do we use a specific `gan_critic` model architecture rather than ResNet to build discriminator?
	- what kind of loss do we use here?
	- what is spectral normalization to make GAN work?
	- maybe we could make a ResNet with spectral normalization to replace `gan_critic`
	- how to train the critic
	- [image:C82EBF3E-0DAD-487B-96D6-0DF587286F76-76996-0002F6C426E9DFFA/D2675782-151B-4BE5-8A91-170D7C868D5F.png]
[/details]
[details="GAN是如何在generator 和 discriminator 之间反复训练的"]

### How to use GAN to do pingpong with generator and discriminator training
70:08- 73:05
[How to use GAN to do pingpong with generator and discriminator training](https://ytcropper.com/cropped/DG5c63b270c1045)
How to use `GANLearner.from_learners` to train the ping pong process?
How `weights_gen` combine both losses (`pixel MSE` and `binaryEntropyLoss`) together to balance generator and the critic?
Why and how to downplay `momentum` when use `Adam`?
	- [image:7321EE22-B189-47AE-B7CA-EB65AEF00CED-76996-0002F93E289E4CA9/0A83E2DD-B404-41E5-A5D8-B1FE3E637856.png]
How to understand the `gen_loss` and `disc_loss` during the training? (one gets better and the other gets worse, and vice versa)
How to show the result of gan training?
	- [image:C16059DC-7061-4621-ADB9-68F9CB0ADB33-76996-0002F99336D4EBFC/778D82F1-55F6-46B9-8A1B-A2FDFC96EB68.png]

[/details]
[details="问答：什么时候需要用U-net"]

### Q&A: when use to U-net or not? 
74:47-75:56
[when use to U-net or not](https://ytcropper.com/cropped/DG5c63bc4de5c6d)
	- segmentation and high resolution
	- classification make no sense
[/details]
[details="WGAN能做什么"]

### What can WGAN do?
75:56-78:37
[How can WGAN do](https://ytcropper.com/cropped/DG5c63ca366d778)
What does WGAN aim to do?
What does generator aim to train a noise image into?
Does WGAN use any pretrained model? NO
After hours, some bedroomish images can be produced eventually
[/details]
[details="如何用GAN来让模型学会识别猫眼"]

### How to train GAN to pay attention to cat’s eyes
[why cat’s eye features can’t be upgraded with current GAN?](https://ytcropper.com/cropped/DG5c63c8577cc08)
73:05-74:47

[How to implement feature loss paper to help](https://ytcropper.com/cropped/DG5c63d6b263d24)
78:37-97:06

[How to use the perceptual loss paper idea to solve the problem](https://ytcropper.com/cropped/DG5c63dab396923)
78:37-83:49
	- How exactly does the style loss and content loss help to capture eye features?
	- do we really do GAN still now? (seems not)

[How to implement the perceptual loss paper into `FeatureLoss` function?](https://ytcropper.com/cropped/DG5c63eabaab98a)
83:52-88:54
	* how to do crappification for this model?
	* which the loss or base loss to pick? which loss does Jeremy like better?
	* How to grab all the feature layers of pretrained VGG model?
	* how to get all the layers for generating features losses?
	* how to create the feature loss or perceptual loss?

[How to train and test on our U-net with feature loss model?](https://ytcropper.com/cropped/DG5c63ed3b7be98)
88:54-93:25
	- how to train a U-net with feature loss
	- how to refactor `do_fit`to make the process easier a little
	- how to train to improve performance
	- test the model with larger images

[What can we be creative with U-net + GAN + feature_loss notebook?](https://ytcropper.com/cropped/DG5c63ef4c33cce)
93:00-97
[image:3F83E9B6-CCF5-4BB7-91D3-008E50AFF678-76996-000305FCE24409DE/0AC75F18-A7C0-42EA-8410-FD9EEC5D54DB.png]
	* What Jason’s crappification approach? 
	* What is deOldify doing?
	* what should we learn and do about crappification and deOldify?

[/details]
[details="如何手写RNN"]


## How to create RNN models from scratch
97:00-119:00
[How to create RNN from scratch](https://ytcropper.com/cropped/DG5c622bd3a6e4b)
[/details]
[details="我们在第一部分里学到了些什么？"]

### What we have learnt in part 1? 
97:00-98:41
[What we have learnt in part 1](https://ytcropper.com/cropped/DG5c625315cc840)
How to link all the concepts below to pain a brief picture of deep learning workflow?
[image:7BE0220B-A7E5-471D-AAEF-B571901C66B6-76996-0002CD2B80C48B99/96AB3B59-287C-4127-83A6-E138EA601D64.png]
	- people usually have to watch the lesson three times to get all the details and feel comfortable with those key concepts
[/details]
[details="如何在图上画出一个隐藏层的神经网络"]

### How to represent basic NN with single hidden layer with diagram?
98:34-100:22
[How to represent basic NN with single hidden layer with diagram](https://ytcropper.com/cropped/DG5c625b71cf22c)
[image:54EB7701-8A48-4AD7-8165-97B9ECAA8B39-76996-0002CF0A4228A58B/AC0913D7-E16D-477F-B4C1-57387524EA8C.png]
	- make sure you are comfortable with how to calculate the shape of the input, activations, and output
[/details]
[details="如何用全链接层模型预测第3第4个字"]

### How to predict 3rd or 4th word with fully connected NN diagram
100:02-103:12
[How to predict 3rd or 4th word with fully connected NN diagram](https://ytcropper.com/cropped/DG5c626d7999fb8)
	- How do fully connected NN use two words to predict the third?
	- How then to predict the fourth word?
	- why should same color parameters should be the same set of parameters?
[image:A3DB17E3-AB76-4818-A1BF-D767C7B646DE-76996-0002D85254D25DE9/BECCCC16-C799-41D3-943B-EBC449BEDA64.png] [image:2EBD0725-7D53-4292-9E85-CCD47C02242F-76996-0002D857FC4B16B9/B4551F3D-468F-4721-9A70-BCA8BF561B96.png]

[/details]
[details="如何用human numbers数据集来构建训练和验证集"]

### RNN Toy example - how to create the training and validation sets from human numbers dataset?
103:09-109:11
[Toy example - how to create the training and validation sets](https://ytcropper.com/cropped/DG5c627a291d07a)
	- how to access the number of tokens in validation set?
	- how to distinguish `bs=batch_size`, `bptt=backpropagation through time`, `num_batches`?
	- How to get 3 batches of data from validation set one by one?
	- How to count the number of elements within a batch of x or y?
	- Why `bptt=70` but first batch has 95 elements and second batch as 69 elements?
	- How `x1` and `y1` differ from each other?
	- How to `textify` numbers into words?
	- How mini-batches of x join up with each other? 
[image:AE5A0EB9-4737-49D4-A96D-5D7F639C6795-76996-0002D54E2D48B6B0/22BDBA2A-B966-420D-8A35-C0FD52358568.png] [image:18BC726D-3B3A-425F-A1FD-056D96B27B76-76996-0002D55B8C6BCD68/A55BC1CA-08A8-4410-A760-E044A17C636E.png] 
[image:F0C85252-1AFF-453A-82C2-16D1F13119F5-76996-0002D564FBB255BD/384FE658-537D-45BC-AF0D-850578C3D6D0.png] [image:90F9A20B-F518-490F-9589-E642B14FEA94-76996-0002D56F65054CFA/DB6FB9FD-D207-470E-9069-631F54B9992A.png] [image:8617D414-3D73-472F-8A61-0D7A74FD76B1-76996-0002D57EE9EF1C9F/280A1DD4-0F34-4ED1-8063-951DF0C4258E.png]
[/details]
[details="如何按照上述结构图来构建模型预测第N和第N-1个字"]

### How to build the predicting n-th from n-1 words model based on the diagram above
108:57-112:08
[How to build the predicting n-th from n-1 words model based on the diagram above](https://ytcropper.com/cropped/DG5c62aaaa7a6e9)
	* How to implement the diagram into a NN?
	* When is appropriate to refractor code?
	* Why RNN can be seen as actually the NN with refactor?
	* How to create a tensor container for `h` the activation?
	* Why the `h` the activation shape should be a fixed size? (just assume to be in the video)

[image:3559F672-B354-4F89-9B4C-3BAF03458589-76996-0002D67E54EA29E7/392E6C24-BDAD-499F-8179-C84AFFA17A3B.png] [image:FEBC5FE9-71E0-4759-BBAC-DB98CB7FD8D2-76996-0002D6BE424D17C4/76DF1742-C01A-4065-8994-3FC590FF12FF.png]
[/details]
[details="如何构建神经网络来预测第N和第N-1个字"]

### How to build the NN to predict N-th word with N-1th word?
112:08-115:00
[How to build the NN to predict N-th word with N-1th word](https://ytcropper.com/cropped/DG5c62b07912c02)
	- How can such model’s loss function make the most out of words input (compared to previous model)?
		- [image:115D0079-23B3-41B6-A52C-1F49EAAAFE22-76996-0002D8B1CA8E7878/EDE758BD-BEB8-4B1C-97C3-8A5821C2C0D0.png]
	* What does the diagram and the NN look like now?
		*  [image:AD60460F-79F2-4AB9-A62B-7CEA27DEE907-76996-0002D8CF71CAF5D2/AF0DF661-4D14-4855-AA30-B80D8CE0325D.png] [image:05A5B6D4-9590-40E1-8E68-A7F5A0C0C163-76996-0002D8DAE81AD37C/0B17DF53-3B3B-46E0-8038-765B09D66A52.png]
	- Why this new model has a worse performance?
		- [image:B58A024E-E6D2-40F4-BC31-7CCEAAD717F1-76996-0002D8EC63A82D9B/9770EC6E-5046-417C-80FD-09132DBB0B24.png]
	- How to solve this problem?
		- [image:602586BF-3EC6-4B5C-9CD6-598BC7BB0E66-76996-0002D909E79C817B/1E5F7C06-85C4-4307-BBC8-E7B0454BC1EB.png][image:0D53D28C-C4CA-4315-A73D-D0D6FC0553B4-76996-0002D920A624A226/606BD09D-1FD6-493C-BFCF-4457923C4DCF.png]
	* So, what is RNN?
		* just fully connected NN with refactor of loops
[/details]
[details="如何构建多层RNN"]

### How to construct multi-layer RNN?
115:00-119:00
[How to construct multi-layer RNN](https://ytcropper.com/cropped/DG5c62bec8985c2)
	- How to refactor the code to with `nn.RNN`? 
		- [image:FBD17C9F-E448-4C70-9667-7518665CE381-76996-0002DBFE40EF2337/A2496C4A-EB7C-4FE3-8A7B-7183F6F24527.png]
	- How to construct a 2-layer RNN?
	- What is GRU or LSTM
		- [image:98B2640C-1011-4FBC-B3CF-7A9D7F02D8BC-76996-0002DC3F7C828DAD/3E17705E-BFA2-4FC7-8CBF-FAC8D15AFC9E.png] [image:23733A06-1A7D-42C7-935E-2BC9BFAE7045-76996-0002DC47DC4EE864/F2D891A4-8012-461A-8814-6BEC49DEC1B1.png]
	* What are sequence labeling tasks?
	* What and how to do NLP classification?
[/details]
[details="如何用心学好"]

## How to learn by heart
1:58:59-end
[How to learn by heart](https://ytcropper.com/cropped/DG5c622f316432f)
### What is it like of watching lessons again and again?
	- a second time can always help to get some bit of the lesson previously not understood and enable to implement some code which was not able to previously

[/details]
[details="为什么我们应该写和分享代码"]

### Why should I write and share codes?
	- make sure you code something on your own
	- people can confirm what you did right and where to improve and learn more
[/details]
[details="为什么以及如何读论文"]

### Why and How to read papers?
	- more papers to cover in part 2
	- just focus on practical sections such as “why we are solving this problem” and “what are the results”

[/details]
[details="用博客写什么"]

### What to write on blogs?
	- put into words on what you learnt 
	- not for DL academic professionals 
	- but to help people like you 6 months ago
[/details]
[details="如何利用论坛"]

### What to do on forums?
	- to get help from others
	- to help others 
	- to share your successful stories
[/details]
[details="为什么以及如何做到一起学"]

### Why and how to get together with your peers?
	- social learning is very helpful
	- we can do book clubs, meetups, study groups
[/details]
[details="为什么以及如何做些东西"]

### Why and how to build something?
	- make the world a slightly better place 
	- or, make people you love a little more delight
	- just finish something, build something, such as a model can generate tweet sounds like Elon Musk
	- people on forum can help even guide you to do so
	- you can build an app, create a project, help with library
[image:9D096B6E-14A0-40E2-AB84-41EB42F1ABC5-76996-0002CB13B44C88BA/FD9C3647-BCE9-47D8-BB36-8EF64F8D9356.png] 
[/details]
[details="如何参与fastai library 建设"]

### How to get involved with fastai library?
	- it may seem boring from outside
	- help docs, texts require deep understanding of the implementation of codes
	- curators can send you papers and materials to figure out why they wrote code this way
	- eventually you are going to write the docs and texts to explain it clearly
[image:E6B8B10E-1561-469E-B457-9EB422A37EA0-76996-0002CB1789E76F94/391148FC-2619-4F2E-AF71-F7E7C064E926.png]
[/details]
[details="如何启动学习小组"]

### How to initiate a study group?
	- go on to forum and find your timezone
	- get a google sheet to sign up 
	- to create projects and wiki together

[/details]
[details="我们会从part2中学到什么？"]

### What to expect from part 2 fastai?
	- see how the fastai codebase was built from stage to stage
	- talking about software development in terms of fastai
	- to learn the process of doing research and reading papers
	- how to turn math into codes
	- many more advanced architectures
[image:48B3388F-1A6C-4D5F-B31D-BFF092F6F724-76996-0002CC48AABA35C9/18DAEBA0-62B4-4E4A-84A0-DF8DC9AC6ECD.png]

[/details]
[details="Jeremy的工做状态是怎样的？以及如何平衡生活与工作"]

### What Jeremy’s typical daylight is like? How to manage work and life?
	- people shocked to see me disorganized and incompetent
	- have a good time without a specific plan, just want to finish it
	- DL is not like web app with regular feedback and specific milestones, therefore you must be able to have fun in DL to keep you going
	- No meetings, phone calls, coffee, TV, PC games, but a lot of time coding, reading, exercising and with family
	- make sure to get something finished properly, and even get a group to do it together

[/details]
[details="机器学习深度学习的哪些领域让你兴奋，为什么不是强化学习"]

### What part of ML DL most exciting to you and why not RL?
	- RL is overly complex and less useful to normal people in day to day work
	- Transfer learning has always been under appreciated and researched, help changed NLP with transfer learning. I am excited to get transfer learning work better and faster in many areas
[/details]
[details="在part2开始前该做什么"]

### What to recommend to practice before part 2?
	- just coding and code all the time
	- make sure you know all the tiny coding skills we covered 
	- rebuild all the notebooks from scratch but with fastai lib
	- it makes you top edge students or practioners
[/details]
[details="fastai5年之后会是什么样子"]

### What is fastai going to be in 5 years?
	- become a software to use without coding
	- get rid of course and code and do useful stuff easily and nicely
[/details]

