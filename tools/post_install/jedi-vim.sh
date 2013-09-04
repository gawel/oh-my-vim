#!/bin/sh
# fetch submodules

cd $HOME/.vim/bundle/jedi-vim
git submodule init
git submodule update
