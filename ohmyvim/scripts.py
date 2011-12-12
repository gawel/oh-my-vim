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
import json
import sys
import os

VIMRC = '''
" added by oh-my-vim

" path to oh-my-vim binary (take care of it if you are using a virtualenv)
let g:ohmyvim="%(binary)s"

" Use :OhMyVim profiles to list all available profiles
let profiles = ['defaults']

" load oh-my-vim
source %(ohmyvim)s

" end of oh-my-vim required stuff

" put your custom stuff bellow

'''


class Bundle(object):

    def __init__(self, manager, dirname):
        self.manager = manager
        self.dirname = dirname
        self.name = basename(dirname)
        self.use_git = isdir(join(dirname, '.git'))
        self.use_hg = isdir(join(dirname, '.hg'))
        self.valid = self.use_hg or self.use_git

    def log(self, *args):
        self.manager.log(*args)

    @property
    def themes(self):
        themes = []
        if isdir(join(self.dirname, 'colors')):
            themes = os.listdir(join(self.dirname, 'colors'))
            themes = [t[:-4] for t in themes]
        return themes

    @property
    def remote(self):
        os.chdir(self.dirname)
        if self.use_git:
            p = Popen(['git', 'remote', '-v'], stdout=PIPE)
            p.wait()
            remote = p.stdout.read().split('\n')[0]
            remote = remote.split('\t')[1].split(' ')[0]
            return remote
        elif self.use_hg:
            p = Popen(['hg', 'path'], stdout=PIPE)
            p.wait()
            remote = p.stdout.read().split('\n')[0]
            remote = remote.split(' = ')[1].strip()
            return remote

    def upgrade(self):
        if self.use_git:
            p = Popen(['git', 'pull', '-qn'], stdout=PIPE)
        elif self.use_hg:
            p = Popen(['hg', 'pull', '-qu'], stdout=PIPE)
        p.wait()

    @property
    def dependencies(self):
        if isfile(join(self.dirname, 'requires.txt')):
            with open(join(self.dirname, 'requires.txt')) as fd:
                return set([d.strip() for d in fd.readlines() if d.strip()])
        return set()

    @classmethod
    def resolve_url(self, url):
        config = get_config()

        url = url.strip()
        url = config.bundles.get(url.lower(), url)
        url = config.vimscripts.get(url.lower(), url)
        return url

    @classmethod
    def install(cls, manager, url):
        url = cls.resolve_url(url)

        use_hg = False
        use_git = False

        if url.startswith('hg+'):
            use_hg = True
            url = url[3:]
        elif url.startswith('git+'):
            use_git = True
            url = url[4:]
        elif len(url.split('/')) == 2:
            url = 'https://github.com/%s/%s.git' % tuple(url.split('/'))
        elif '://github.com' in url and not url.endswith('.git'):
            url = url.replace('http://', 'https://').rstrip() + '.git'

        if url.endswith('.git'):
            use_git = True
            use_hg = False

        dirname = cmd = None

        if use_git:
            name = basename(url)[:-4]
            dirname = join(manager.runtime, name)
            cmd = ['git', 'clone', '-q', url, dirname]
        elif use_hg:
            name = basename(url.strip('/'))
            dirname = join(manager.runtime, name)
            cmd = ['hg', 'clone', '-q', url, dirname]
        else:
            manager.log('%s is not a valid url', url)

        if dirname and isdir(dirname):
            manager.log('%s already installed.', name)
        elif cmd:
            manager.log('Installing %s...', name)
            Popen(cmd).wait()
            b = cls(manager, dirname)
            return b


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

        ohmyvim = join(self.ohmyvim, 'ohmyvim.vim')
        if not isfile(ohmyvim):
            with open(ohmyvim, 'w') as fd:
                fd.write('source %s\n' % join(self.runtime, 'vim-pathogen',
                                                   'autoload', 'pathogen.vim'))
                fd.write('call pathogen#runtime_append_all_bundles()\n')
                fd.write('source %s\n' % join(self.ohmyvim, 'theme.vim'))

        if 'VIRTUAL_ENV' in os.environ:
            binary = join(os.getenv('VIRTUAL_ENV'), 'oh-my-vim')
        else:
            binary = 'oh-my-vim'
        kw = dict(ohmyvim=ohmyvim, binary=binary)
        if not isfile(expanduser('~/.vimrc')):
            with open(expanduser('~/.vimrc'), 'w') as fd:
                fd.write(VIMRC % kw)
        else:
            with open(expanduser('~/.vimrc')) as fd:
                if ohmyvim not in fd.read():
                    with open(expanduser('~/.vimrc'), 'a') as fd:
                        fd.write(VIMRC % kw)

    def log(self, value, *args):
        if args:
            value = value % args
        self.output.append(value)
        sys.stdout.write(value + '\n')
        sys.stdout.flush()

    def get_bundles(self):
        bundles = []
        for plugin in os.listdir(self.runtime):
            bundle = Bundle(self, join(self.runtime, plugin))
            if bundle.valid:
                bundles.append(bundle)
        return bundles

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
        if '__ohmyvim_test__' not in os.environ:
            webbrowser.open_new(url)
        else:
            self.log(url)

    def info(self, args):
        url = Bundle.resolve_url(args.bundle)
        if url.endswith('.git'):
            url = url[:-4]
        url += '#readme'
        if '__ohmyvim_test__' not in os.environ:
            webbrowser.open_new(url)
        else:
            self.log(url)

    def list(self, args):
        for b in self.get_bundles():
            if args.raw:
                self.log(b.name)
            else:
                if args.urls:
                    if b.name not in self.dependencies:
                        if b.use_git:
                            self.log('git+%s', b.remote)
                        elif b.use_hg:
                            self.log('hg+%s', b.remote)
                else:
                    self.log('* %s (%s)', b.name, b.remote)
        if args.all:
            config = get_config()
            for name, url in sorted(config.bundles.items()):
                self.log('- %s (%s)', name, url)
            for name, url in sorted(config.vimscripts.items()):
                self.log('- %s (%s)', name, url)

    def install(self, args):
        config = get_config()
        if args.raw:
            for name in sorted(config.bundles.keys()):
                self.log(name)
            for name in sorted(config.vimscripts.keys()):
                self.log(name)
        else:
            dependencies = set()
            for url in args.url:
                if url.endswith('.txt'):
                    if isfile(url):
                        with open(url) as fd:
                            dependencies = [d for d in fd.readlines()]
                    elif url.startswith('http'):
                        fd = urlopen(url)
                        dependencies = dependencies.union(
                                            set([d for d in fd.readlines()]))
                else:
                    b = Bundle.install(self, url)
                    if b:
                        dependencies = dependencies.union(b.dependencies)
            if dependencies:
                self.log('Processing dependencies...')
                for url in dependencies:
                    if url.strip():
                        b = Bundle.install(self, url.strip())

    def upgrade(self, args):
        for b in self.get_bundles():
            if b.name in args.bundle or len(args.bundle) == 0:
                self.log('Upgrading %s...', b.name)
                b.upgrade()

    def remove(self, args):
        if args.bundle:
            for b in self.get_bundles():
                if b.name in args.bundle:
                    if b.name in self.dependencies:
                        self.log("Don't remove %s!", b.name)
                    self.log('Removing %s...', b.name)
                    shutil.rmtree(b.dirname)

    def theme(self, args):
        theme = args.theme
        if theme:
            for b in self.get_bundles():
                if theme in b.themes:
                    self.log('Activate %s theme...', theme)
                    with open(join(self.ohmyvim, 'theme.vim'), 'w') as fd:
                        fd.write(':colo %s\n' % theme)
        else:
            for b in self.get_bundles():
                themes = b.themes
                if themes:
                    if args.raw:
                        for theme in themes:
                            self.log(theme)
                    else:
                        self.log('* %s (%s)', b.name, b.remote)
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


def get_config():
    filename = join(os.path.dirname(__file__), 'config.ini')
    return ConfigObject(filename=filename)


def main(*args):
    import argparse

    manager = Manager()

    parser = argparse.ArgumentParser(description='Oh my Vim!')
    subparsers = parser.add_subparsers(help='sub-command help')

    p = subparsers.add_parser('search')
    p.add_argument('-t', '--theme-only', action='store_true', default=False)
    p.add_argument('term', nargs='*', default='')
    p.set_defaults(action=manager.search)

    p = subparsers.add_parser('info',
                              help='try to open the web page of the bundle')
    p.add_argument('bundle', default='')
    p.set_defaults(action=manager.info)

    p = subparsers.add_parser('list')
    p.add_argument('--raw', action='store_true', default=False)
    p.add_argument('-a', '--all', action='store_true', default=False)
    p.add_argument('-u', '--urls', action='store_true', default=False)
    p.set_defaults(action=manager.list)

    p = subparsers.add_parser('install', help='install a script or bundle')
    p.add_argument('--raw', action='store_true', default=False)
    p.add_argument('url', nargs='*', default='')
    p.set_defaults(action=manager.install)

    p = subparsers.add_parser('upgrade', help='upgrade bundles')
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

    return manager.output


def update_registry():
    vimscripts = {}
    links = 'https://api.github.com/users/vim-scripts/repos; rel="next"'
    while 'rel="next"' in links:
        url = links.split(';')[0].strip(' <>')
        print('Loading %s...' % url)
        resp = urlopen(url)
        repos = json.loads(resp.read())
        vimscripts.update([(r['name'], r['clone_url']) for r in repos])
        links = resp.headers.get('Link', '')

    config = get_config()
    config.vimscripts = vimscripts
    config.write()
