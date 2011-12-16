#!/bin/sh

OHMYVIM=$HOME/.oh-my-vim
export PATH=$PATH:$OHMYVIM/bin



buildout() {
    mkdir -p $OHMYVIM/eggs
    if ! [ -f "bootstrap.py" ]
    then
        wget -c "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"
    fi
    python bootstrap.py --distribute --eggs=$OHMYVIM/eggs
    $OHMYVIM/bin/buildout
}

install_node() {

    NODE=`which node`

    if ! [ -x "$NODE" ]
    then
        ! [ -x "`which gcc`" ] && return
    fi

    if [ -x $NODE ]
    then
        binary="binary=$NODE"
    else
        binary=""
    fi

    mkdir -p $OHMYVIM/node
    cd $OHMYVIM/node
    cat << EOF > $OHMYVIM/node/buildout.cfg
[buildout]
parts = node
eggs-directory=$OHMYVIM/eggs
bin-directory=$OHMYVIM/bin
[node]
recipe = gp.recipe.node
npms =
    coffee-script
    csslint
    jslint
    less
scripts =
    csslint
    jslint
    coffee
    cake
    lessc
$binary
EOF
    buildout
}

