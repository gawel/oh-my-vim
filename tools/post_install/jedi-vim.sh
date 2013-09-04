#!/bin/sh
# fetch submodules

cd $HOME/.vim/bundle/jedi-vim
git submodules init
git submodules update
