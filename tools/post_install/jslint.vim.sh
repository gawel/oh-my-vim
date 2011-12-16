#!/bin/bash

. $HOME/.vim/bundle/oh-my-vim/tools/functions.sh


if ! [ -x "`which node`" ]
then
    install_node
fi
