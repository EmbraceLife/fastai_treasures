alias ex='cd /Users/Natsume/Documents/experiments; conda activate fastai'
alias ft='cd /Users/Natsume/Documents/fastai_treasures/; conda activate fastai'
alias v3='cd /Users/Natsume/Documents/course-v3/nbs/dl1; conda activate fastai'
alias fk='cd /Users/Natsume/Documents/fastai-fork; conda activate fastai'
alias sfastai='cd /Users/Natsume/Documents/fastai-fork/fastai/; conda activate fastai'
alias spython='cd ~/miniconda3/envs/fastai/lib/python3.7/; conda activate fastai'
alias pdbpp='python -m pdb'
alias de='conda deactivate'
alias xcode="open -a Xcode"
alias typora="open -a typora"
alias jn='jupyter notebook'


function lazygit() {
    git add .
    git commit -a -m "$1"
    git push
}

function lazyupdate() {
    git fetch upstream
    git checkout master
    git merge --no-edit upstream/master
    git push

}

export PS1="\w "







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
