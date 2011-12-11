from os.path import join
from os.path import isdir
from os.path import isfile
from os.path import basename
from os.path import expanduser
from ConfigObject import ConfigObject
from urllib import urlopen
from subprocess import Popen
from subprocess import PIPE
from glob import glob
import webbrowser
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

    dependencies = {
        'vim-pathogen': 'https://github.com/tpope/vim-pathogen.git',
        'oh-my-vim': 'https://github.com/gawel/oh-my-vim.git',
      }

    def __init__(self):
        self.output = []

        self.runtime = expanduser('~/.vim/bundle')
        self.autoload = expanduser('~/.vim/autoload')
        self.ohmyvim = expanduser('~/.vim/ohmyvim')

        for dirname in (self.runtime, self.autoload,
                        self.ohmyvim, expanduser('~/.vim/swp')):
            if not isdir(dirname):
                os.makedirs(dirname)

        for name, url in self.dependencies.items():
            if not isdir(join(self.runtime, name)):
                Popen(['git', 'clone', '-q', url,
                       join(self.runtime, name)]).wait()

        if not isfile(join(self.ohmyvim, 'theme.vim')):
            with open(join(self.ohmyvim, 'theme.vim'), 'w') as fd:
                fd.write('')

        if not isfile(join(self.ohmyvim, 'ohmyvim.vim')):
            with open(join(self.ohmyvim, 'ohmyvim.vim'), 'w') as fd:
                fd.write('source %s\n' % join(self.runtime, 'vim-pathogen',
                                                   'autoload', 'pathogen.vim'))
                fd.write('call pathogen#runtime_append_all_bundles()\n')
                fd.write('source %s\n' % join(self.ohmyvim, 'theme.vim'))

        kw = dict(ohmyvim=join(self.ohmyvim, 'ohmyvim.vim'),
                  binary=os.path.abspath(sys.argv[0]))
        if not isfile(expanduser('~/.vimrc')):
            with open(expanduser('~/.vimrc'), 'w') as fd:
                fd.write(VIMRC % kw)
        else:
            with open(expanduser('~/.vimrc')) as fd:
                if kw['binary'] not in fd.read():
                    with open(expanduser('~/.vimrc'), 'a') as fd:
                        fd.write(VIMRC % kw)

    def log(self, value, *args):
        if args:
            value = value % args
        self.output.append(value)
        print(value)

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
        url = ("https://github.com/search?"
               "langOverride=&repo=&start_value=1&"
               "type=Repositories&language=VimL&q=") + terms
        if '__test__' not in os.environ:
            webbrowser.open_new(url)
        else:
            self.log(url)

    def list(self, args):
        for plugin, dirname, themes in self.get_plugins():
            if args.complete:
                self.log(plugin)
            else:
                os.chdir(dirname)
                p = Popen(['git', 'remote', '-v'], stdout=PIPE)
                p.wait()
                remote = p.stdout.read().split('\n')[0]
                remote = remote.split('\t')[1].split(' ')[0]
                if args.urls:
                    if plugin not in self.dependencies:
                        self.log(remote)
                else:
                    self.log('* %s (%s)', plugin, remote)

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
                self.log('%s already installed. Upgrading...', name)
                os.chdir(dirname)
                Popen(['git', 'pull', '-n']).wait()
            else:
                self.log('Installing bundle %s...', name)
                Popen(['git', 'clone', '-q', url, dirname]).wait()
            if isfile(join(dirname, 'requires.txt')):
                with open(join(dirname, 'requires.txt')) as fd:
                    dependencies = [d for d in fd.readlines()]
        else:
            self.log('%s is not a git url', url)
        return dirname, dependencies

    def install(self, args):
        filename = join(os.path.dirname(__file__), 'config.ini')
        config = ConfigObject(filename=filename)
        if args.complete:
            for name in sorted(config.bundles.keys()):
                self.log(name)
            for name in sorted(config.themes.keys()):
                self.log(name)
        else:
            dependencies = set()
            for url in args.url:
                url = config.bundles.get(url, url)
                url = config.themes.get(url, url)
                if url.endswith('.txt'):
                    if isfile(url):
                        with open(url) as fd:
                            dependencies = [d for d in fd.readlines()]
                    elif url.startswith('http'):
                        fd = urlopen(url)
                        dependencies = [d for d in fd.readlines()]
                else:
                    _, deps = self.install_url(url)
                    for d in deps:
                        if d.strip():
                            dependencies.add(d)
            if dependencies:
                self.log('Processing dependencies...')
                for url in dependencies:
                    self.install_url(url)

    def upgrade(self, args):
        for plugin, dirname, themes in self.get_plugins():
            if plugin in args.bundle or 'all' in args.bundle:
                self.log('Upgrading %s...', plugin)
                os.chdir(dirname)
                Popen(['git', 'pull', '-n']).wait()

    def remove(self, args):
        if args.bundle:
            for plugin, dirname, themes in self.get_plugins():
                if plugin in args.bundle:
                    if plugin in self.dependencies:
                        self.log("Don't remove %s!", plugin)
                    self.log('Removing %s...', plugin)
                    dirname = join(self.runtime, plugin)
                    if isdir(join(dirname, '.git')):
                        shutil.rmtree(dirname)

    def theme(self, args):
        theme = args.theme
        if theme:
            for plugin, dirname, themes in self.get_plugins():
                if theme in themes:
                    self.log('Activate %s theme...', theme)
                    with open(join(self.ohmyvim, 'theme.vim'), 'w') as fd:
                        fd.write(':colo %s\n' % theme)
        else:
            for plugin, dirname, themes in self.get_plugins():
                if isdir(join(dirname, '.git')):
                    os.chdir(dirname)
                    p = Popen(['git', 'remote', '-v'], stdout=PIPE)
                    p.wait()
                    remote = p.stdout.read().split('\n')[0]
                    remote = remote.split('\t')[1].split(' ')[0]
                if themes:
                    if args.complete:
                        for theme in themes:
                            self.log(theme)
                    else:
                        self.log('* %s (%s)', plugin, remote)
                        self.log('\t- %s', ', '.join(themes))

    def profiles(self, args):
        profiles = join(self.runtime, 'oh-my-vim', 'profiles')
        profiles = glob(join(profiles, '*.vim'))

        for profile in sorted(profiles):
            name = basename(profile)[:-4]
            if not name.startswith('.'):
                desc = ''
                with open(profile) as fd:
                    line = fd.readline()
                    if line.startswith('"'):
                        desc += line.strip(' "\n')
                if desc:
                    self.log('* %s - %s', name, desc)
                else:
                    self.log('* %s', name)


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
    p.add_argument('--complete', action='store_true', default=False)
    p.add_argument('-u', '--urls', action='store_true', default=False)
    p.set_defaults(action=manager.list)

    p = subparsers.add_parser('install', help='install a script or bundle')
    p.add_argument('--complete', action='store_true', default=False)
    p.add_argument('url', nargs='*', default='')
    p.set_defaults(action=manager.install)

    p = subparsers.add_parser('upgrade', help='upgrade bundles')
    p.add_argument('bundle', nargs='*', default='')
    p.set_defaults(action=manager.upgrade)

    p = subparsers.add_parser('remove', help='remove a bundle')
    p.add_argument('bundle', nargs='*', default='')
    p.set_defaults(action=manager.remove)

    p = subparsers.add_parser('theme', help='list or activate a theme')
    p.add_argument('--complete', action='store_true', default=False)
    p.add_argument('theme', nargs='?', default='')
    p.set_defaults(action=manager.theme)

    p = subparsers.add_parser('profiles', help='list all available profiles')
    p.set_defaults(action=manager.profiles)

    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    args.action(args)

    return manager.output
