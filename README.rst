Oh My Vim!
===========

This package allow you to manage your vim plugins

It's heavily inspired from `oh-my-zsh
<https://github.com/robbyrussell/oh-my-zsh>`_

Installation
============

You must have `python3.X <http://www.python.org>`_ installed on your system.

It's recommended to install **oh-my-vim** as a non root user.

If you don't know python and virtualenv then just run the install script::

    $ curl https://raw.github.com/gawel/oh-my-vim/master/tools/install.sh | sh -

Or with wget::

    $ wget --no-check-certificate -O- https://raw.github.com/gawel/oh-my-vim/master/tools/install.sh | sh -


If you know virtualenv/pip then run this in a virtualenv::

    $ pip install oh-my-vim
    $ bin/oh-my-vim upgrade

Have a look at your ``~/.vimrc``::

    $ vim ~/.vimrc

And select your favorites profiles.

Commands
========

Browse all VimL projects available on github in your favorite browser::

    $ oh-my-vim search [-t] [term]

Installation. You can use a git url or a ``requires.txt`` file/url wich
contains git urls::

    $ oh-my-vim install [--full] [giturl|requires.txt]

The ``--full`` options allow to install some extra dependencies. For example
`syntastic <https://github.com/scrooloose/syntastic#readme>`_ require `flake8
<http://pypi.python.org/pypi/flake8>`_ and `jslint
<https://github.com/reid/node-jslint>`_. **oh-my-vim** will try to install them
for you.

Remove a bundle::

    $ oh-my-vim remove [bundle1|bundle2|...]

List installed packages::

    $ oh-my-vim list

List all packages listed in Oh My Vim's registry::

    $ oh-my-vim list -a

Generate a ``requires.txt`` file::

    $ oh-my-vim list -u > requires.txt

Upgrade bundles (and **oh-my-vim** python package)::

    $ oh-my-vim upgrade [--full] [bundle1|bundle2|...]

Useful links
============

- `Vim revisited <http://mislav.uniqpath.com/2011/12/vim-revisited/>`_

- `Vim for programmers <http://i.snag.gy/r7ExK.jpg>`_

FAQ
===

**I'm a newbie. Can oh-my-vim turn me into a Vim guru ?**

No, but it can help you to setup a friendly environment.

After the installation step install some `useful
<https://github.com/gawel/oh-my-vim/tree/master/tools/requires/useful.txt>`_
plugins with the following::

    $ oh-my-vim install -d useful

Then have a look at the `defaults
<https://github.com/gawel/oh-my-vim/tree/master/profiles/default.vim>`_ and
`map <https://github.com/gawel/oh-my-vim/tree/master/profiles/map.vim>`_
profiles and enable them in your ``.vimrc``

You're now ready to go...!

**What if I already use pathogen ?**

Nothing. Just remove the ``pathogen`` stuff from your ``vimrc``

**Can I use oh-my-vim from Vim ?**

Yes, and you should. You'll get some completion. Just use ``:OhMyVim <args>``

**Can I install a bundle from a mercurial repository ?**

Yes. You just need to prefix your url with ``hg+``::

  $ oh-my-vim install hg+https://bitbucket.org/sjl/gundo.vim

**Good project but I'm missing a feature. Can you add it ?**

No. But you can. Fork the repository and submit a pull request.

**I have a cool plugin and I want to add it to oh-my-vim-registry**

Submit a pull request after adding it to the `registry
<https://github.com/gawel/oh-my-vim/blob/master/ohmyvim/config.ini>`_

**Does oh-my-vim work on windows ?**

No, it wont be so hard to port but I'm not supporting this OS

**This is a great project. Can I offer you a beer ?**

Sure.

