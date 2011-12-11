from os.path import join
from os.path import isdir
from os.path import isfile
from os.path import abspath
from os.path import basename
from os.path import expanduser
from urllib import urlopen
from subprocess import Popen
from subprocess import PIPE
import webbrowser
import subprocess
import shutil
import sys
import os

VIMRC = '''
" added by oh-my-vim
let g:ohmyvim="%(binary)s"

" Use :OhMyVim profiles to list all available profiles
let profiles = ['defaults']

" load oh-my-vim
source %(ohmyvim)s
'''

class Manager(object):

    runtime = expanduser('~/.vim/bundle')
    autoload = expanduser('~/.vim/autoload')
    ohmyvim = expanduser('~/.vim/ohmyvim')

    dependencies = {
        'vim-pathogen': 'https://github.com/tpope/vim-pathogen.git',
        'oh-my-vim': 'https://github.com/gawel/oh-my-vim.git',
      }

    def __init__(self):
        for dirname in (self.runtime, self.autoload, self.ohmyvim):
            if not isdir(dirname):
                os.makedirs(dirname)
        for name, url in self.dependencies.items():
            if not isdir(join(self.runtime, name)):
                Popen(['git', 'clone', url, join(self.runtime, name)]).wait()
        if not isfile(join(self.ohmyvim, 'theme.vim')):
            with open(join(self.ohmyvim, 'theme.vim'), 'w') as fd:
                fd.write('')
        if not isfile(join(self.ohmyvim, 'ohmyvim.vim')):
            with open(join(self.ohmyvim, 'ohmyvim.vim'), 'w') as fd:
                fd.write('source %s\n' % join(self.runtime, 'vim-pathogen',
                                                   'autoload', 'pathogen.vim'))
                fd.write('call pathogen#runtime_append_all_bundles()\n')
                fd.write('source %s\n' % join(self.ohmyvim, 'theme.vim'))
        ohmyvim = join(self.ohmyvim, 'ohmyvim.vim')
        binary = os.path.abspath(sys.argv[0])
        if not isfile(expanduser('~/.vimrc')):
            with open(expanduser('~/.vimrc'), 'w') as fd:
                fd.write(VIMRC % locals())
        else:
            with open(expanduser('~/.vimrc')) as fd:
                if binary not in fd.read():
                    with open(expanduser('~/.vimrc'), 'a') as fd:
                        fd.write(VIMRC % locals())

    def get_plugins(self):
        plugins = []
        for plugin in os.listdir(self.runtime):
            dirname = join(self.runtime, plugin)
            if isdir(join(dirname, '.git')):
                themes = []
                if isdir(join(dirname, 'colors')):
                    themes = os.listdir(join(dirname, 'colors'))
                    themes = [t[:-4] for t in themes]
                plugins.append((plugin, dirname, themes))
        return plugins

    def search(self, args):
        terms = [t.strip() for t in args.term if t.strip()]
        if args.theme_only:
            terms.insert(0, 'colorschemes')
        if not terms:
            terms = ['language%3AVimL']
        terms = '%20'.join(terms)
        webbrowser.open_new(("https://github.com/search?"
                             "langOverride=&repo=&start_value=1&"
                             "type=Repositories&language=VimL&q=") + terms)

    def list(self, args):
        for plugin, dirname, themes in self.get_plugins():
            if args.raw:
                print plugin
            else:
                os.chdir(dirname)
                p = Popen(['git', 'remote', '-v'], stdout=PIPE)
                p.wait()
                remote = p.stdout.read().split('\n')[0]
                remote = remote.split('\t')[1].split(' ')[0]
                if args.urls:
                    if plugin not in self.dependencies:
                        print remote
                else:
                    print '* %s (%s)' % (plugin, remote)

    def install_url(self, url):
        url = url.strip()
        dependencies = []
        dirname = None
        if '://github.com' in url and not url.endswith('.git'):
            url = url.replace('http://', 'https://').rstrip() + '.git'
        if url.endswith('.git'):
            name = basename(url)[:-4]
            dirname = join(self.runtime, name)
            if os.path.isdir(dirname):
                print '%s already installed. Upgrading...' % name
                os.chdir(dirname)
                Popen(['git', 'pull']).wait()
            else:
                print 'Installing bundle %s...' % name
                Popen(['git', 'clone', url, dirname]).wait()
            if isfile(join(dirname, 'requires.txt')):
                with open(join(dirname, 'requires.txt')) as fd:
                    dependencies = [d for d in fd.readlines()]
        else:
            print '%s is not a git url' % url
        return dirname, dependencies

    def install(self, args):
        dependencies = set()
        for url in args.url:
            if url.endswith('requires.txt'):
                if isfile(url):
                    with open(url) as fd:
                        dependencies = [d for d in fd.readlines()]
                elif url.startswith('http'):
                    fd = urlopen(url)
                    dependencies = [d for d in fd.readlines()]
            else:
                for _, d in self.install_url(url):
                    if d.strip():
                        dependencies.add(d)
        if dependencies:
            print 'Processing dependencies...'
            for url in dependencies:
                 self.install_url(url)

    def upgrade(self, args):
        if not args.bundle:
            print 'all'
        for plugin, dirname, themes in self.get_plugins():
            if plugin in args.bundle or 'all' in args.bundle:
                print 'Upgrading %s...' % plugin
                os.chdir(dirname)
                Popen(['git', 'pull']).wait()
            elif args.raw:
                print plugin


    def remove(self, args):
        for plugin, dirname, themes in self.get_plugins():
            if not args.bundle:
                print plugin
            elif plugin in args.bundle:
                if plugin in self.dependencies:
                    print "Don't remove %s!" % plugin
                print 'Removing %s...' % plugin
                dirname = join(self.runtime, plugin)
                if isdir(join(dirname, '.git')):
                    shutil.rmtree(dirname)

    def theme(self, args):
        theme = args.theme
        if theme:
            if theme.startswith('http'):
                theme_dir, _ = self.install_url(theme)
                for plugin, dirname, themes in self.get_plugins():
                    if theme_dir == dirname and len(themes) == 1:
                        theme = themes[0]
                        print 'Activate %s theme...' % theme
                        with open(join(self.ohmyvim, 'theme.vim'), 'w') as fd:
                            fd.write(':colo %s\n' % theme)
            else:
                for plugin, dirname, themes in self.get_plugins():
                    if theme in themes:
                        print 'Activate %s theme...' % theme
                        with open(join(self.ohmyvim, 'theme.vim'), 'w') as fd:
                            fd.write(':colo %s\n' % theme)
            return
        for plugin, dirname, themes in self.get_plugins():
            if isdir(join(dirname, '.git')):
                os.chdir(dirname)
                p = Popen(['git', 'remote', '-v'], stdout=PIPE)
                p.wait()
                remote = p.stdout.read().split('\n')[0]
                remote = remote.split('\t')[1].split(' ')[0]
            if themes:
                if args.raw:
                    for theme in themes:
                        print theme
                else:
                    print '* %s (%s)' % (plugin, remote)
                    print '\t- %s' % ', '.join(themes)

    def profiles(self, args):
        profiles = join(self.runtime, 'oh-my-vim', 'profiles')
        profiles = [join(profiles, p) for p in os.listdir(profiles)]

        for profile in sorted(profiles):
            name = basename(profile)[:-4]
            desc = ''
            with open(profile) as fd:
                line = fd.readline()
                if line.startswith('"'):
                    desc += line.strip(' "\n')
            if desc:
                print '* %s - %s' % (name, desc)
            else:
                print '* %s' % name


def main(*args):
    import argparse

    manager = Manager()

    parser = argparse.ArgumentParser(description='Oh my Vim!')
    subparsers = parser.add_subparsers(help='sub-command help')

    p = subparsers.add_parser('search')
    p.add_argument('-t', '--theme-only', action='store_true', default=False)
    p.add_argument('term', nargs='*', default='')
    p.set_defaults(action=manager.search)

    p = subparsers.add_parser('list')
    p.add_argument('--raw', action='store_true', default=False)
    p.add_argument('-u', '--urls', action='store_true', default=False)
    p.set_defaults(action=manager.list)

    p = subparsers.add_parser('install', help='install a script or bundle')
    p.add_argument('url', nargs='*', default='')
    p.set_defaults(action=manager.install)

    p = subparsers.add_parser('upgrade', help='upgrade bundles')
    p.add_argument('--raw', action='store_true', default=False)
    p.add_argument('bundle', nargs='*', default='')
    p.set_defaults(action=manager.upgrade)

    p = subparsers.add_parser('remove', help='remove a bundle')
    p.add_argument('bundle', nargs='*', default='')
    p.set_defaults(action=manager.remove)

    p = subparsers.add_parser('theme', help='list or activate a theme')
    p.add_argument('--raw', action='store_true', default=False)
    p.add_argument('theme', nargs='?', default='')
    p.set_defaults(action=manager.theme)

    p = subparsers.add_parser('profiles', help='list all available profiles')
    p.set_defaults(action=manager.profiles)

    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()
    args.action(args)


