#!/bin/sh

set -e

py=`which python3`

echo "Using $py"

ohmyvim="bin/oh-my-vim"
install_dir=$HOME/.oh-my-vim
bundles=$HOME/.vim/bundle
mkdir -p $install_dir
cd $install_dir

if ! [ -d "$install_dir/bin" ]
then
    echo "Installing pyvenv using $pyvenv..."
    $py -m venv .
fi

! [ -d $bundles ] && mkdir -p $bundles

. $install_dir/bin/activate

pip=$install_dir/bin/pip

echo "Installing dependencies..."
$pip install -q ConfigObject argparse

echo "Installing ranger..."
$pip install -q --src="$HOME/.vim/bundle/" \
    -e "git+https://github.com/hut/ranger.git@master#egg=ranger"

echo "Installing oh-my-vim..."
if [ -d $HOME/.vim/bundle/oh-my-vim ]; then
    $pip install -q -e "$HOME/.vim/bundle/oh-my-vim"
else
    $pip install -q --src="$HOME/.vim/bundle/" \
        -e "git+https://github.com/gawel/oh-my-vim.git@master#egg=oh-my-vim"
fi

$install_dir/bin/oh-my-vim version > /dev/null
version=`$install_dir/bin/oh-my-vim version`

echo "Sucessfully installed oh-my-vim $version to $install_dir"
echo "Binary can be found at $install_dir/$ohmyvim"

add_path() {
    if [ "`grep $install_dir $1`" = "" ]
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

