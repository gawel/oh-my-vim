#!/bin/sh
py=$(which python2.6 || which python2.7)

if ! [ -x $py ]
then
    echo "Can't find a python interpreter"
    exit
fi

echo "Using $py"

ohmyvim="bin/oh-my-vim"
install_dir=$HOME/.oh-my-vim
bundles=$HOME/.vim/bundle
mkdir -p $install_dir
cd $install_dir

if ! [ -d "$install_dir/bin" ]
then
    echo "Installing virtualenv..."
    venvurl='https://raw.github.com/pypa/virtualenv/master/virtualenv.py'
    curl -sO $venvurl || wget --no-check-certificate -c $venvurl
    $py virtualenv.py -q --distribute env
fi

! [ -d $bundles ] && mkdir -p $bundles

source $install_dir/env/bin/activate

echo "Installing dependencies..."
pip install -q ConfigObject argparse

echo "Installing oh-my-vim..."
pip install -q --src="$HOME/.vim/bundle/" \
    --install-option="--script-dir=$install_dir/bin" \
    -e "git+https://github.com/gawel/oh-my-vim.git@master#egg=oh-my-vim"

$install_dir/bin/oh-my-vim version > /dev/null
version=$($install_dir/bin/oh-my-vim version)

echo ""
echo "=========================================================="
echo "Sucessfully installed oh-my-vim $version to $install_dir"
echo "Binary can be found at $install_dir/$ohmyvim"

function add_path() {
    if [ "$(grep $install_dir $1)" == "" ]
    then
        echo "Adding $install_dir/bin to \$PATH in $1"
        cat << EOF >> $1
# Added by oh-my-vim
export PATH=\$PATH:$install_dir/bin

EOF
    echo "Now source it!"
    echo ""
    echo "    source $1"
    fi
}

if [ -f ~/.zshrc ]
then
    add_path ~/.zshrc
elif [ -f ~/.bashrc ]
then
    add_path ~/.bashrc
else
    echo ""
    echo "!! Please add $install_dir/bin to your \$PATH"
    echo ""
    echo "    export PATH=\$PATH:$install_dir/bin"
fi
echo ""
echo "========================================================"

