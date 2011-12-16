#!/bin/sh

. $HOME/.vim/bundle/oh-my-vim/tools/functions.sh

if ! [ -x "`which flake8`" ]
then
    if [ -x "$PIP" ]
    then
        $PIP install flake8
    else
        echo "You must install flake8 if you want python support"
    fi
fi

if ! [ -x "`which tidy`" ]
then
    echo "You need to install tidy to get xhtml syntax check"
fi

for b in "coffee" "jslint" "lessc" "csslint"
do
    if ! [ -x "`which $b`" ]
    then
        echo "Let's try to install $b..."
        install_node
        exit
    fi
done

