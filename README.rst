Oh My Vim!
===========

This package allow you to manage your vim plugins

It's eavily inspired from `oh-my-zsh
<https://github.com/robbyrussell/oh-my-zsh>`_

Installation
============

Just run::

    $ pip install oh-my-vim

Install from the repository::

    $ pip install -e "git+https://github.com/gawel/oh-my-vim.git#egg=oh-my-zsh"


Commands
========

Search on github::

    $ oh-my-vim search [-t] term

Installation. You can use a git url or a ``requires.txt`` file/url wich
contains git urls::

    $ oh-my-vim install [giturl|requires.txt]

Remove a bundle::

    $ oh-my-vim remove [bundle1|bundle2|...]

List installed packages::

    $ oh-my-vim list

Generate a ``requires.txt`` file::

    $ oh-my-vim list -u > requires.txt

Upgrade bundles::

    $ oh-my-vim upgrade [bundle1|bundle2|...]

