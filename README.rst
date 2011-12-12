Oh My Vim!
===========

This package allow you to manage your vim plugins

It's eavily inspired from `oh-my-zsh
<https://github.com/robbyrussell/oh-my-zsh>`_

Installation
============

It's recommended to install ``oh-my-vim`` as a non root user.

Just run::

    $ pip install oh-my-vim

Install from the repository::

    $ pip install -e "git+https://github.com/gawel/oh-my-vim.git#egg=oh-my-zsh"

Add the ``--upgrade`` option for upgrading.

If ``oh-my-vim`` is installed as root. You'll have to upgrade your user account::

    $ oh-my-vim upgrade all

Have a look at your ``~/.vimrc``::

    $ vim ~/.vimrc

And select your favorites profiles.

Commands
========

Browse all VimL projects available on github in your favorite browser::

    $ oh-my-vim search [-t] [term]

Installation. You can use a git url or a ``requires.txt`` file/url wich
contains git urls::

    $ oh-my-vim install [giturl|requires.txt]

Remove a bundle::

    $ oh-my-vim remove [bundle1|bundle2|...]

List installed packages::

    $ oh-my-vim list

List all packages listed in Oh My Vim's registry::

    $ oh-my-vim list -a

Generate a ``requires.txt`` file::

    $ oh-my-vim list -u > requires.txt

Upgrade bundles::

    $ oh-my-vim upgrade [bundle1|bundle2|...]

Notice that you'd better use ``pip install --upgrade oh-my-vim`` to get a clean
update. This will also update all bundles.

Useful links
============

- `Vim revisited <http://mislav.uniqpath.com/2011/12/vim-revisited/>`_

- `Vim for programmers <http://i.snag.gy/r7ExK.jpg>`_

FAQ
===

**Can I use oh-my-vim from Vim ?**

Yes, and you should. You'll get some completion. Just use ``:OhMyVim <args>``

**Can I install a bundle from a mercurial repository ?**

Yes. You just need to prefix your url with ``hg+``::

  $ oh-my-vim install hg+https://bitbucket.org/sjl/gundo.vim

**This is a great project. Can I offer you a beer ?**

Sure.

**Good project but I'm missing a feature. Can you add it ?**

No. But you can. Fork the repository and submit a pull request.

**I have a cool plugin and I want to add it to oh-my-vim-registry**

Submit a pull request after adding it to the `registry
<https://github.com/gawel/oh-my-vim/blob/master/ohmyvim/config.ini>`_

