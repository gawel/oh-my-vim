#!/bin/sh
# fetch submodules

cd $HOME/.vim/bundle/jedi-vim
git --git-dir=.git submodule init
git --git-dir=.git submodule update
