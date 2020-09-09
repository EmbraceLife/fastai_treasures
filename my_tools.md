
# My toolbox 我的本地设置

- 如何不commit下，对Kaggle kernel大型文件下载 [论坛分享 ](https://forums.fast.ai/t/platform-kaggle-kernels/32569/139?u=daniel)
- 如何给你的code snippet做快捷键 [论坛分享](https://forums.fast.ai/t/jupyter-notebook-enhancements-tips-and-tricks/17064/27?u=daniel)
- 如何做你的第一个文档改进PR [听写](https://forums.fast.ai/t/fast-ai-v3-2019/39325/88?u=daniel)
- 如何创建你的第一个多行代码snippet [论坛分享](https://forums.fast.ai/t/jupyter-notebook-enhancements-tips-and-tricks/17064/28?u=daniel)
- 我的[快捷键设置](https://github.com/EmbraceLife/fastai_treasures/tree/master/my_shortcut_src)



## Recent found resources

- [10 basic vim command](http://www.oualline.com/vim/10/top_10.html)      
- [how to use mac to snapshot screen](http://www.techadvisory.org/2014/09/4-screenshot-tips-for-mac/)     
- [how to get apps side by side](https://support.apple.com/en-us/HT204948)
- [vim medium](https://medium.com/usevim/vim-101-quick-movement-c12889e759e0)     

# vscode editor

### how to add html snippet
- shift+cmd+p : Preferences: configure user snippet
- open html.json
- add the following codes into the most outward `{}`
```json
"html simple": {
    "prefix": "html simple",
    "body": [ 
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
            "<title>$1</title>",
        "</head>",
        "<body>",
            "  $2",
        "</body>",
        "</html>"
    ]
}
```

# Atom editor

### how to view git diff of each commit
- Atom git extension is great to view the difference of each commit

### how to see blame git in Atom
- add `better git blame`
- but to view the history we have to go to github instead

### how to use vim in Atom
- add `vim mode plus`
- it should incorporate with your current vim usage ok

### how to do multiple cursor editing
```bash
`shift + V, j, k` = to select
`shift + I, j, k` = to activate multiple cursor and move around
`a` or `i` = to insert
`ecs`, `ecs` = to exist multiple cursor mode
```

### how to search files in the directory
- `shift+cmd+p` => `Fuzzy fider`
- `toggle file finder` => `cmd+P`

### folding and unfolding code
- `alt/option+cmd+shift+[` = fold all codes
- `alt+cmd+[` = fold immediate
- `ctrl+alt+cmd+F` = fold selection

### Hydrogen keyboard shortcuts
- `alt+cmd+backspace` = clear results
- `ctrl+cmd+enter` = run all
- run above = select and run
- import notebook
- export notebook

### How to fold in markdown Writer
https://github.com/zhuochun/md-writer/blob/master/package.json#L21
- `shift+cmd+p`: search keymaps
- `ctrl + 1` = folder header 1
- `ctrl + 2` = folder header 2
- `ctrl + 3` = folder header 3

### most used atom keyboard shortcuts
https://github.com/nwinkler/atom-keyboard-shortcuts

### How to create snippets
https://flight-manual.atom.io/using-atom/sections/snippets/
```bash
'.source.js':
  'console.log':
    'prefix': 'log'
    'body': 'console.log(${1:"crash"});$2'

'.source.js':
  'if, else if, else':
    'prefix': 'ieie'
    'body': """
      if (${1:true}) {
        $2
      } else if (${3:false}) {
        $4
      } else {
        $5
      }
      """    

'.source.gfm':
  'Hello World':
    'prefix': 'hewo'
    'body': 'Hello World!'

  'Github Hello':
    'prefix': 'gihe'
    'body': 'Octocat says Hi!'

  'Octocat Image Link':
    'prefix': 'octopic'
    'body': '![GitHub Octocat](https://assets-cdn.github.com/images/modules/logos_page/Octocat.png)'
```

### How to find and replace phrases across files
```bash
shift + cmd + F
# Note: use reg to narrow on files such as *.py on the third row
# open more project folders to allow cross projects search
```

# NVM basics

### How to monitor fastai-v2 source code changes
- download nodemon
```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
```
- set the env: just copy and paste the three lines into terminal
```bash
# Node Version Manager
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```
- install the stable version
```
nvm install stable
nvm use stable
```
- keep dev folder ipynb monitored and update the changes to source code
```bash
npm i -g nodemon
nodemon -e ipynb --exec python notebook2script.py
```

# Terminal basics

### change folder for mac snapshot
- `defaults write com.apple.screencapture location ~/Documents/doc-v2/dev/images`

### How to copy a whole folder to another folder
```bash
cp -a /source/. /dest/
```

### remove a folder or a file

```bash
rm -rf my-dir # to remove an entire folder
rm my-file
```

### 如何在iterm2中切屏分屏跳跃
`shift` + `cmd` + `d` = 横切屏幕      
`opt` + `cmd` + `up/down arrow` = 跳屏      
`cmd` + `w` = 关屏      



### 最常用的terminal commands
```bash
# find out the size of directory folders
du -sh *  
# move cursor to the front or end of a line
ctrl + a = to the end of a line
ctrl + e = to the start of a line
ctrl + u = clear the line before the cursor
ctrl + k = clear the line after the cursor
cmd + k = clear the terminal
ctrl + f = move forward a character
ctrl + b = backward
# go to preference, profile, keys, make right `option` key equivalent to `+ESC`
option + f = move forward by a word
option + b = move backward by a word
ctrl + w = remove a word before cursor
option + d = remove a word after cursor
```




### 构建bash_profile
reload bash_profile with `source ~/.bash_profile`

```bash
alias ftrans='cd /Users/Natsume/Documents/fastai_courses_translation_EN2CN; conda activate fastai'
alias exp='cd /Users/Natsume/Documents/fastai-contrib/; git checkout doc_source; cd py-examples; conda activate fastai'
alias ft='cd /Users/Natsume/Documents/fastai_treasures/my_workstation/; conda activate fastai'
alias v3='cd /Users/Natsume/Documents/course-v3/; git checkout myv3; cd nbs/py-dl1; conda activate fastai; vim $(fzf)'
alias fk='cd /Users/Natsume/Documents/fastai-contrib/; conda activate fastai'
alias sfastai='cd /Users/Natsume/Documents/fastai-contrib/fastai/; conda activate fastai; git checkout doc_source; vim $(fzf)'
alias spython='cd ~/miniconda3/envs/fastai/lib/python3.7/site-packages; conda activate fastai; vim $(fzf)'
alias storch='cd /Users/Natsume/miniconda3/envs/fastai/lib/python3.7/site-packages/torch; conda activate fastai; vim $(fzf)'
alias pdbpp='python -m pdb'
alias de='conda deactivate'
alias xcode="open -a Xcode"
alias atom="open -a atom"
alias typora="open -a typora"
alias jn='jupyter notebook'
alias branch='git checkout'
alias fvim='vim $(fzf)'

function lazygit() {
    git add .
    git commit -a -m "$1"
    git push
}

function lazyupdate() {
    git checkout master
    git fetch upstream
    git checkout master
    git merge --no-edit upstream/master
    git push

}

function lazybranch() {
    git checkout master
    git branch "$1"
    git checkout "$1"
    git push --set-upstream origin "$1"
}

function lazydelete(){
    git checkout master
    git branch -D "$1"
    git push origin --delete "$1"

}

function lazymerge(){
    git merge master
    git add .
    git commit -a -m "$1"
    git push

}

export PS1="\w "
#export PS1="untar_data "






export LC_ALL=zh_CN.UTF-8
export LANG=zh_CN.UTF-8

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

# added by Anaconda3 5.2.0 installer
export PATH="/anaconda3/bin:$PATH"
# added by Miniconda3 4.5.12 installer
# >>> conda init >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$(CONDA_REPORT_ERRORS=false '/Users/Natsume/miniconda3/bin/conda' shell.bash hook 2> /dev/null)"
if [ $? -eq 0 ]; then
    \eval "$__conda_setup"
else
    if [ -f "/Users/Natsume/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/Natsume/miniconda3/etc/profile.d/conda.sh"
        CONDA_CHANGEPS1=false conda activate base
    else
        \export PATH="/Users/Natsume/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda init <<<
# added by Miniconda3 4.5.12 installer
# >>> conda init >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$(CONDA_REPORT_ERRORS=false '/Users/Natsume/miniconda3/bin/conda' shell.bash hook 2> /dev/null)"
if [ $? -eq 0 ]; then
    \eval "$__conda_setup"
else
    if [ -f "/Users/Natsume/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/Natsume/miniconda3/etc/profile.d/conda.sh"
        CONDA_CHANGEPS1=false conda activate base
    else
        \export PATH="/Users/Natsume/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda init <<<

```

# Vim basics

### how to check docs for Ag
```bash
:h Ag
```

### how to install ctag
```bash
brew install ctag
```

### clever ways of inserting
https://vi.stackexchange.com/questions/5634/what-options-are-there-to-enter-insert-mode/5635#5635?newreg=832229f9e2ae41db99ed8afb864bb0da
```bash
c: Delete text (and yank to the buffer) and enter insert mode.
cc: Delete the line and enter insert mode.
C: Delete until the end of the line and enter insert mode.
s: Delete a number of characters and enter insert mode.
S: Delete a number of line and enter insert mode.
```
other ways of doing insert
```bash
i: Insert before the cursor.
I: Insert before the first non-blank character of the line.
a: Insert after the cursor.
A: Insert at the end of the line.
o: Begin a new line below the current line and insert.
O: Begin a new line above the current and insert.
gI: Insert at column 1 of the line.
gi: Insert where insert mode was last stopped.
```

### comment out (not working)
- `shift v`
- `shift i`
- `#`

### unlimited undos
see https://unix.stackexchange.com/questions/192212/vim-how-to-trace-back-all-changes-done-to-file-during-the-day

### see changes recently made to a file
- `:changes` to see a list of changes
- `g;` = go to previous changes
- `g,` = go to next changes
- line-number `g;` = go to the line of changes

### to copy a line from one file to another
- open one file in vim
- `ctrl + w` + `v` to open another split
- `:e ~/Document/...` to find another file and enter to open
- then you can do copy and paste as a technique shown below

### to delete a word
- type `dw`

### copy or replace a line
- `shift + v` to select a line
- `y` to copy
- go to another line and `shift + v` to select
- `p` to replace

### copy a word
- move cursor onto a word
- type `yiw` to copy the word
- move cursor to where you want
- type `ciw` `ctrl + r ` `esc` to paste


### repeat commands
```vim
. = to repeat command without :
@: = to repeat command with :
: + up-down-arrow = browse previous commands and change as you like
```

### Search multiple files with `fzf` and `ag`

https://github.com/rking/ag.vim
https://github.com/junegunn
```vim
vim $(fzf)
ctrl c = to close fzf
ctrl jk = move up down

:Ag _make_subclass
```

### Search multiple files with `grep`
https://codeyarns.com/2017/09/13/grep-cheatsheet/
use long string to narrow down
```vim
:grep -R _make_subclass * # search for rare strings
:copen
:cclose
:cn
:cp
```

### vim switching locations and commands
```vim
ctrl + o = jump to previous location
ctrl + i = jump to forward location
q: = command history
j or k = select commands
: + up-down-arrow = switch between commands
```

### install kite for vim

- install Kite
- select vim as editor during installation process
- go to local setting and install vim and neovim plugins
- then ready to use kite with vim



### vim cursor moving
```bash

0 = go to start of a line
$ = go to end of a line
H = go to top of a window
L = go to bottle of a window
M = go to middle of a window
G = go to the end of a file
gg = go to the first line of a file
20G = go to the 20th line of a file
e = next word
b = previous word
( = previous sentence
) = next sentence
{ = previous paragraph or block
} = next paragraph or block
`` = go to previous edit place
```



### Vim kick start

learnt from this [video](https://www.youtube.com/watch?v=ggSyF1SVFr4) by tutorialLinux

```bash
:q = just quit
:w = save
:wq = save and quit
:q! = quit without saving
i = go into insert mode to write code
ecs = go back to command mode
dd = from command mode to delete a line
3dd = delete 3 lines
u = undo last action
ctrl + r = redo action
/search_word = to search a word inside a file
n = to move to the next finding of your search
shift + n = to move back the previous finding
:%s/search_word/replace_word/gc = replace one by one
:%s/search_word/replace_word/g = replace all at once
```

simple workflow

-  use search to go around quicky and i to insert and u to delete


### vim 如何用上下键跳跃5行代码
go to .vimrc, copy the following
```vim
noremap <Up> 5k
noremap <Down> 5j
```
then, just use arrow up or down



### 用vim找pdbpp中运行的代码 vim find codelines in pdbpp
0. :find folder/filename
1. press esc
2. type line number
3. `shift + g`



### vim如何剪切，复制，粘贴，保存
vim如何剪切，复制，粘贴，保存
```vim
: how to cut, under normal mode
: 1. put cursor to where you want to cut
: 2. press v and move cursor to select characters
: 2. press V and move cursor to select lines
: 3. press d to cut, press y to copy
: 4. move to where to paste,
: 5; press P to paste before cursor
: 5: press p to paset after cursor
: 6. insert mode, press :w and enter
```


### 如何做vim常规搜索
文本内如何做vim常规搜索
[Searching | Vim Tips Wiki | FANDOM powered by Wikia](http://vim.wikia.com/wiki/Searching)
```vim
/ls   ;; 我们在搜索ls, 前面不要有space空格
?*.ls
/path.ls
;; inside .vimrc
set ignorecase
```




### vim如何对文件夹做tag

```vim
; terminal文件夹下输入 vim
; 再输入 :MT

; 尝试搜索untar_data
:tag untar ;tab to complete
```

### Explore source code, split screen, vim


```vim
; 将鼠标放在要探索的code上
ctrl + w, v = same file on two vertical screens
ctrl + ] ;= dive in
ctrl + t ;= pull back
ctrl + w, ctrl + ] ;= dive in from another horizontal split
ctrl + w, up or dn or lt or rt arrows;= switch between splits
ctrl + \ ;= dive in from a new tab
ctrl + a, ;left or right ;= switch between tabs
:q = to quit any split screen
```

### vim 如何寻找文件和文件夹搜索
```vim
:find pathlib ; 寻找pathlib所在文件
- ; 调入上一级文件夹路径
:b# ; 从打开的文档中跳回上一次打开的路径
:tag Path ; 进入文件后再搜索
```

### vim 如何展开和折叠

```vim
za ;将鼠标放在+-
```

### vim 如何知道当前所在文件地址
```vim
:F ; tab to complete and enter
```


### 安装下载 vim
```bash
brew install vim
brew upgrade vim
vim # to run vim
```

### 设置 vim source
```bash
nano ~/.vimrc
```

### 安装 ctags
```bash
brew install ctags

```

### .vimrc file

```vim
call plug#begin('~/.vim/plugged')
Plug '/usr/local/opt/fzf'
Plug 'junegunn/fzf.vim'
Plug 'junegunn/fzf', { 'dir': '~/.fzf', 'do': './install --all' }
Plug 'junegunn/fzf.vim'
call plug#end()

let g:ackprg = 'ag --nogroup --nocolor --column'

set rtp+=~/.fzf
set tags=tags
set foldcolumn=3
set foldmethod=indent
set ignorecase
set number

command FileAddress echo expand('%:p')

syntax on
set background=dark
filetype indent plugin on

""""" current millenium
set nocompatible
syntax enable
filetype plugin on

""""" file finder or fuzzy search
set path+=**

""""" display all matching files when tab
set wildmenu

""""" Tag Jumping
command! MakeTags !ctags -R .
command MT MakeTags

""""" tag jump with new tab horizontally or vertically
map <C-\> :tab split<CR>:exec("tag ".expand("<cword>"))<CR>

"""" switch tabs in vim
map <C-a><up> :tabr<cr>
map <C-a><down> :tabl<cr>
map <C-a><left> :tabp<cr>
map <C-a><right> :tabn<cr>

""""" map bb to :cp, map ff to :cn
map rr :@:<cr>
map ff ::cn<cr>
map bb ::cp<cr>

""""" map arrow up to go up 5 lines and down to go down 5 lines
noremap <Up> 5k
noremap <Down> 5j

"""""""""""""""" make presentation with vim files
au VimEnter no_plugins.vim setl window=66
au VimEnter no_plugins.vim normal 8Gzz
au VimEnter no_plugins.vim command! GO normal M17jzzH
au VimEnter no_plugins.vim command! BACK normal M17kzzH
au VimEnter no_plugins.vim command! RUN execute getline(".")
" au VimEnter no_plugins.vim unmap H
" au VimEnter no_plugins.vim unmap L
" why dont these work :(
au VimEnter no_plugins.vim nnoremap ^f :GO<CR>
au VimEnter no_plugins.vim nnoremap ^b :BACK<CR>

""""" export Grep_Path="~/.vim/plugin/grep"

"""""" undo for a whole day
set undodir=~/.vim/undodir
set undofile
set undolevels=1000
set undoreload=10000
set runtimepath^=~/.vim/bundle/ag

```

# Git basics

### Change git config editor
```bash
git config core.editor vim
```

### How to move back to old commit permanently?
https://stackoverflow.com/questions/3293531/how-to-permanently-remove-few-commits-from-remote-branch
```bash
git reset --hard <last_working_commit_id>
git push --force

```


### How to ignore a file in git and see differences
https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository

```bash
echo tag >> .git/info/exclude # to ignore tag

git add .
git diff --staged
```

### How to push a local folder to a remote git repo
```
# go to your local folder in terminal
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/EmbraceLife/doc_torch.git
git push -u origin master

```

### How to resolve conflict in git
https://stackoverflow.com/questions/161813/how-to-resolve-merge-conflicts-in-git



head is my current version
master is the version I want to merge with
the === seperate the two versions differences
```py
1 <<<<<<< HEAD
2 open an issue
3 ======
4 ask your question in IRC.
5 >>>>>>> master
```

to resolve:
1. you make the final changes to HEAD on line 2
2. remove the following lines
```py
1 <<<<<<< HEAD
3 =======
4 ask your question in IRC.
5 >>>>>>> master
```

### check out the difference
```bash
git diff @^ # previous and current difference
git diff previous-commit-id # older commit and current difference
git diff # unstaged difference
git diff --cache # staged difference
git diff HEAD # all changes unstaged and staged
```

### How to change commit messages
#### before push it
```bash
git commit --amend
# then recommit and push
```

#### after push it
```bash
# after the previous steps
git push --force doc_source
```

#### older commit
```bash
git rebase -i HEAD~n # n commits

```

### Encountered problems
- [Build Fails](https://forums.fast.ai/t/documentation-improvements/32550/183?u=daniel)
    - in general, we can ignore it.

### 如何使用git merge
```bash
git help merge # to check out how to use git merge
# inside exp branch by `git checkout exp`, run the following to merge with master
git merge master
# then run `git commit -a -m "merge"` to finish it up
```


### 如何撤回本地和推送的commit
```bash
git checkout -- filename # 撤回未commit的changes
git reset --hard HEAD~1 # 撤回已经commit的changes
git push origin +master
```

### 如何免去用户名和密码
```bash
# Permanently authenticating with Git repositories
$ git config credential.helper store
$ git push https://github.com/repo.git

Username for 'https://github.com': <USERNAME>
Password for 'https://USERNAME@github.com': <PASSWORD>

```

### 如何快速git push
```bash
# 一步完成
lazygit 'message'

# 分步骤操作
# create a new repo on github
# go to your Mac directory
git init
git add README.md
git commit -m "first commit"
git remote add origin official-repo.git
git push -u origin master
git reset # to undo git add .

```

### 如何在原fastai repo和你的fork repo之间更新？

```bash
# 一步完成
lazyupdate

# 分步骤操作
# step1: fork from official
# step2: git clone from your fork
git clone https://github.com/EmbraceLife/my-fork
cd my_fork
tools/run-after-git-clone # fastai tools
git remote add upstream official-url-git # link to official repo
git remote -v # check all branches local and remote

git pull upstream master # pull from official repo, or
######## suggested by fastai is better I guess
git fetch upstream
git checkout master
git merge --no-edit upstream/master
git push
######## suggested by fastai

git push # update my-fork
git pull # pull from my-fork
```


###  如何创建git branch, make changes and git push to cloud
```

git branch # check all branches
git branch new_branch_name # create a branch from where we are
git branch -m a_new_name # rename
git branch -d branch_to_go # delete
git checkout new_branch # switch to a new branch
# make changes, do commit, then push with the following code, it won't affect master branch!!!
git push --set-upstream origin new-branch-name #
git push origin --delete new_branch_name # to delete a branch remote in github
svn checkout url-folder-replace-tree/master-with-trunk # only download part of a repo

```

# PDBPP basics


### .pdbrc
[如何构建和安装pdbrc video](https://www.bilibili.com/video/av16754002/)
[如何使用pdbpp来实验代码](https://www.bilibili.com/video/av16753161/)

```python
## located at ~ directory, named .pdbrc, no need for source, just save it
alias dr pp dir(%1)
alias cls pp %1.__class__
alias dt pp %1.__dict__
alias pdt for k, v in %1.items(): print(k, ": ", v)
alias dtkeys for k, _ in %1.items(): print(k)
alias loc locals().keys()
alias doc from inspect import getdoc; from pprint import pprint; pprint(getdoc(%1))
alias sources from inspect import getsourcelines; from pprint import pprint; pprint(getsourcelines(%1))
alias module from inspect import getmodule; from pprint import pprint; pprint(getmodule(%1))
alias sig from inspect import signature; from pprint import pprint; pprint(signature(%1))
alias member from inspect import getmembers; from pprint import pprint; pprint(getmembers(%1))
alias members from inspect import getmembers; from pprint import pprint; pprint(dict(getmembers(%1))['%2'])
alias clstree from inspect import getmro; from pprint import pprint; pprint(getmro(%1.__class__))
alias opt_param optimizer.param_groups[0]['params'][%1]

alias opt_grad optimizer.param_groups[0]['params'][%1].grad

```

### .pdbrc.py
```py
"""
This is an example configuration file for pdb++.
Actually, it is what the author uses daily :-). Put it into ~/.pdbrc.py to use
it.
"""

import readline
import pdb

class Config(pdb.DefaultConfig):

    filename_color = pdb.Color.yellow
    truncate_long_lines = False  # so you get all content insight
    highlight = True
    sticky_by_default = True
    line_number_color = pdb.Color.red
    filename_color = pdb.Color.yellow
    use_pygments = True
    bg = 'light'
    current_line_color = 1 # white arrow

```



# Video


### youtube-dl
[youtube-dl](https://github.com/rg3/youtube-dl/blob/master/README.md#readme)

```
--write-sub                      Write subtitle file
--write-auto-sub                 Write automatic subtitle file (YouTube only)
--all-subs                       Download all the available subtitles of the video
--list-subs                      List all available subtitles for the video
--sub-format FORMAT              Subtitle format, accepts formats preference, for example: "srt" or "ass/srt/best"
--sub-lang LANGS                 Languages of the subtitles to download (optional) separated by commas, use IETF language tags like 'en

youtube-dl --write-auto-sub  --sub-lang en  --sub-format srt https://youtu.be/1ZhtwInuOD0

youtube-dl -f 'best[ext=mp4]'  --write-auto-sub  --sub-lang en  --sub-format srt https://www.youtube.com/playlist?list=PLfYUBJiXbdtSIJb-Qd3pw0cqCbkGeS0xn


```
[transcript transform](https://subtitletools.com/convert-to-srt-online)

### Monosnap for video

1. set 5 frame/second
2. high quality
3. capture mouse cursor and clicks
4. it will be small enough
5. it can also create gif from movie too



### 如何将youtube sbv字幕转化为srt
- 在youtube翻译字幕页面下载你的翻译sbv文件
- 前往https://captionsconverter.com/ 做转化
- 前往B站字幕上传你的字幕



### 翻译Youtube字幕常用快捷键
- 将鼠标放置在主输入栏，翻译即可
- `shift` + `space`  = 暂停/播放
- `shift` + `arrow left/right` = 后退/前进
- 如要修改，前往具体字幕栏修改



### 如何去除YouTube字幕翻译时的卡顿

- 先下载空白的YouTube提供的sbv字幕
- 删除所有时间设置
- 再重新上传回去



### Looper for youtube
- chrome extension : looper for youtube
- set automaticall loop all videos




### 如何为视频做语音解说
	- 使用ytcropper做视频截取，循环播放
	- mac音量调到最低
	- 用quicktime做屏幕录制，提供语音解读，音量调节适中



# Jupyter Notebook vs atom

### Update nbviewer right away
```html
github-file-link + ?flush_cache=true
```


### Jupyter notebook extensions

```
conda install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
jupyter nbextension enable toc2/main  # in terminal or notebook cell, both are fine
# edit/notebook_config (at bottom of the droplist)
```


### jn color theme
```
conda install jupyterthemes
jt -t onedork
#| grade3 | oceans16 | chesterish | monokai | solarizedl | solarizedd
```

### use atom with Hydrogen
1. atom core packages
2. install hydrogen and its extensions (may not use at all though)
3. install autocompletion python
3. atom beautify
4. `source activate fastai`
5. go to a folder and then `atom .`


### Jupyter notebook install
```
# If you have Python 3 installed (which is recommended):

python3 -m pip install --upgrade pip
python3 -m pip install jupyter

jupyter notebook # to start
```

# 如何安装fastai workstation

- 下载安装conda
    - [下载最新Conda, Mac选择pkg比较方便](https://conda.io/en/latest/miniconda.html)
    - 双击安装
    - 更新 `conda update conda` # outside conda env
- 创建独立工作环境
    - `conda create -n fastai python=3`  或者明确一个版本3.5
    - `conda activate fastai` 开启实验环境
    - `conda deactivate` 关闭实验环境
    - `conda remove --name fastai --all` 删除环境
- 下载安装pdbpp 适配python 3.6均可3.7（可能只要是fastai dev 版本，就行）
    - `conda install pdbpp` is a must
    - `conda install -c conda-forge pdbpp`
- 下载安装Jupyter notebook
    - 更新 pip:  `python3 -m pip install --upgrade pip`
    - 下载更新Jupyter: `python3 -m pip install jupyter`
- 下载安装 Pytorch和fastai libraries
    - 一步安装：`conda install -c pytorch -c fastai fastai pytorch`
    - 更新  ` conda update conda -y `  outside env
    - 更新 ` conda update -c fastai fastai ` inside env
    - 检验 `conda list` `pip show`
    - 卸载 `conda uninstall fastai`
- 连接官方repo
    ```bash
    git remote add origin https://github.com/fastai/fastai.git
    git remote -v # to check all orign and remote address
    ```

### 如何启用 fastai dev version

- see https://github.com/fastai/fastai#developer-install

```bash
git clone https://github.com/EmbraceLife/fastai.git fastai-contrib
cd fastai-contrib
git remote -v
git remote add upstream https://github.com/fastai/fastai.git
conda uninstall -y fastai # uninstall conda fastai
cd fastai-contrib
tools/run-after-git-clone
pip install -e ".[dev]"
```

### How to update other dependencies for dev fastai
https://forums.fast.ai/t/documentation-improvements/32550/198?u=daniel
```bash
conda install -c pytorch pytorch torchvision # just update pytorch
conda install -c fastai -c pytorch --update-deps fastai # update all dependencies
conda update -c pytorch -c fastai --update-all # equivalent to the above
# if it install fastai in conda again, just uninstall it as it did in previous block of code
```

### install pytorch
go to its official sites for downloading code
```bash
conda install pytorch torchvision -c pytorch # no cuda
```

# Conda Basics

```bash
# download miniconda https://docs.conda.io/en/latest/miniconda.html
conda --version # check version:
conda update conda # update conda: , install outside env
conda create -n mesa-abm python=3.6 anaconda # build environment
source activate mesa-abm
source deactivate
conda info --envs # check envs
conda env list # all envs to view
conda create --name new_env --clone existed_env # clone an env
conda remove --name old_env --all # delete an env
conda env export > environment.yml # 输出env
conda env create -f environment.yml # build env from yml
```


### 如何使用 pdbpp basics
```python
python -m pdb file-name.py
# 原来进入代码，输入insert import pdb; pdb.set_trace() 来debug已经不需要了
sticky # 看到全局代码
ll # 从debug跳回到全局代码
# l 20
# l 1, 20: see line from 1 to 20
s # step into a function
n # 运行下一行
w # call stack, where I started and where I am in source code, d go down a stack, u to go up a stack
b 88 # 运行到88行，暂停
# b file.py:41 or b func_name
# b 11, this_year==2017: conditional breakpoint, at line 11 to breakpoint, if this_year == 2017
cl 1 # 删除第一个breakpoint
r # 运行所在 function
c # 运行直到结束
q # 终止
? # 查看文档
hit return # 重复上一次操作
pp variable_name # 友好打印 该变量
# 完成当前loop: until
plt.show() # print out images
```

# Math

turn any snapshort of math in Latex https://mathpix.com/

- ctrl + cmd + m = to crop


## 其他参考链接

[How to Customize your Terminal Prompt  |   OSXDaily](http://osxdaily.com/2006/12/11/how-to-customize-your-terminal-prompt/)     
[inspect — Inspect live objects — Python 3.7.2 documentation](https://docs.python.org/3/library/inspect.html)    
[20 Terminal shortcuts developers need to know - TechRepublic](https://www.techrepublic.com/article/20-terminal-shortcuts-developers-need-to-know/)

[如何修改谷歌浏览器语言设置for colab](chrome://settings/?search=language)


## JS
- [thoughts](https://github.com/EmbraceLife/learn-svelte/issues/1)
