
# How to do PR for Docs Source

This is a visual guide to do a pull request (PR) on fastai library document source files (ipybn), which will walk you through every step of pushing a PR.

Before you start, you should know the very basics of git. You can learn it from [the terminal guide](https://course.fast.ai/terminal_tutorial.html) on fastai course site.

## Step 1 Get idea support from the forum

When you have an idea on PR, please go to [Documentation improvements](https://forums.fast.ai/t/documentation-improvements/32550) to share your thought and get support.

PR01.png![image.png](PRimages/PR01.png)

## Step 2 Fork and download repo

Please fork the official repo and clone your fork by following the visual guide [here](https://course.fast.ai/terminal_tutorial.html#cloning-fastai-repository-download-the-fastai-files).

## Step 3 Sync your fork and local repo with official repo

First, go to your fork on github to check whether it is updated. If not (seen image below), then you need to sync.

PR02.png![image.png](PRimages/PR02.png)

Then you can go to your terminal and step into your local repo directory (fastai-fork, in this visual example), and sync your local repo and official repo by following the steps in the image below.

PR03.png![image.png](PRimages/PR03.png)

Then you can go to your fork to see whether the sync is a success or not.

PR03.5.png![image.png](PRimages/PR03.5.png)

## step 4 delete and create branches

If you have done PR before, you may want to delete your previous branch locally and on github. In this example, I have a branch called update-freeze-docsrc (see the blue box in the image below).

PR04.png![image.png](PRimages/PR04.png)

You can delete this branch locally and on github by following the first four steps in the image below.     

Then you can proceed with the remaining steps in the image, to create a new branch for your PR, called 'freeze_to' in this example.

PR06.png![image.png](PRimages/PR06.png)

If you refresh the previous branch page on github, it won't be found.

PR05.png![image.png](PRimages/PR05.png)

Also you will find a new branch created on your fork, see the box below.

PR07.png![image.png](PRimages/PR07.png)

## Step 5 Make your edits

You can make your edits of documentation and make it public with Kaggle kernels, so that people on Documentation improvement thread can see and give suggestions.

If you finally decided to make it a PR, then you can proceed to copy the changes onto the original ipynb file in your local repo.

PR08.png![image.png](PRimages/PR08.png)

## Step 6 Push the PR

You can check the changes you made to the original doc source ipynb by running the two lines of codes below.

PR09.png![image.png](PRimages/PR09.png)

Then if the changes seem ok, you can run the following three lines of codes to push the changes to your fork.

PR10.png![image.png](PRimages/PR10.png)

## Step 7 Make a PR

On your fork in github, you can see your push and click the blue box on the right to make a PR.

PR11.png![image.png](PRimages/PR11.png)

You can also add some notes to your PR.

PR12.png![image.png](PRimages/PR12.png)

## Step 8 Coming back to Documentation improvements

Finally, you can come back to the thread for follow-ups, as you may encounter some errors before your PR merged.

PR13.png![image.png](PRimages/PR13.png)


```python

```
