#!/bin/sh
py=$(which python2.6 || which python2.7)

if ! [ -x $py ]
then
    echo "Can't find a python interpreter"
    exit
fi

ohmyvim="bin/oh-my-vim"
install_dir=$HOME/.oh-my-vim
bundles=$HOME/.vim/bundle
mkdir -p $install_dir
cd $install_dir

if ! [ -d "$install_dir/bin" ]
then
    curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    $py virtualenv.py --no-site-packages --distribute .
fi

source bin/activate
! [ -d $bundles ] && mkdir -p $bundles
pip install --upgrade --src="$HOME/.vim/bundle/" -e "git+https://github.com/gawel/oh-my-vim.git#egg=oh-my-vim"
rm -f virtualenv.py* *.tar.gz
version=`oh-my-vim version`
echo "========================================================"
echo "Sucessfully installer oh-my-vim $version to $install_dir"
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
    echo "!! Please add $install_dir/bin to your $PATH"
fi
echo ""
echo "========================================================"

