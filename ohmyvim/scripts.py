from os.path import join
from os.path import isdir
from os.path import isfile
from os.path import basename
from ConfigObject import ConfigObject
from subprocess import Popen
from subprocess import PIPE
from glob import glob
import pkg_resources
import webbrowser
import shutil
import json
import sys
import os

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

VIMRC = '''
" Added by oh-my-vim

" Change the default leader
" let mapleader = ","

" Skip upgrade of oh-my-vim itself during upgrades
" let g:ohmyvim_skip_upgrade=1

" Use :OhMyVim profiles to list all available profiles with a description
" let profiles = %(profiles)r
let profiles = ['defaults']

" Path to oh-my-vim binary (take care of it if you are using a virtualenv)
let g:ohmyvim="%(binary)s"

" load oh-my-vim
source %(ohmyvim)s

" End of oh-my-vim required stuff

" Put your custom stuff bellow

'''

GVIMRC = '''
" uncomment this to set a font
" set guifont="Menlo Regular:h11"

" no bell
set noerrorbells

" window size
if exists(':win')
    win 150 50
endif

" remove menu and toolbar. see help guioptions
set guioptions=aegirlt
'''

GIT_URL = "https://github.com/gawel/oh-my-vim.git"

TOOLS = join(os.path.dirname(__file__), '..', 'tools')


class Bundle(object):

    def __init__(self, manager, dirname):
        self.manager = manager
        self.dirname = dirname
        self.name = basename(dirname)
        self.use_git = isdir(join(dirname, '.git'))
        self.use_hg = isdir(join(dirname, '.hg'))
        self.valid = self.use_hg or self.use_git
        self.home = os.environ['HOME']

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
            stdout, stderr = p.communicate()
            stdout = stdout.decode('utf8')
            remote = stdout.split('\n')[0]
            remote = remote.split('\t')[1].split(' ')[0]
            return remote
        elif self.use_hg:
            p = Popen(['hg', 'path'], stdout=PIPE)
            stdout, stderr = p.communicate()
            stdout = stdout.decode('utf8')
            remote = stdout.split('\n')[0]
            remote = remote.split(' = ')[1].strip()
            return remote

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
    def install(cls, manager, args, url):
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
            cmd = ['git', 'clone', '-q', '-b', 'master', url, dirname]
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
            if args.full:
                b.post_install()
            return b

    def upgrade(self, args):
        self.log('Upgrading %s...', self.name)
        if self.name.lower() == 'oh-my-vim':
            self.self_upgrade()
        else:
            os.chdir(self.dirname)
            if self.use_git:
                p = Popen(['git', 'pull', '-qn', 'origin', 'master'],
                          stdout=PIPE)
                p.wait()
            elif self.use_hg:
                p = Popen(['hg', 'pull', '-qu'], stdout=PIPE)
                p.wait()
            if args.full:
                self.post_install()

    def get_pip(self):
        install_dir = join(self.home, '.oh-my-vim/')
        if os.path.isdir(install_dir):
            bin_dir = join(install_dir, 'env', 'bin')
        else:
            bin_dir = os.path.dirname(sys.executable)
            pip = join(bin_dir, 'pip')
        pip = join(bin_dir, 'pip')
        if os.path.isfile(pip):
            return pip
        return ''

    def post_install(self):
        script = join(TOOLS, 'post_install', '%s.sh' % self.name)
        if not isfile(script):
            script = join(self.dirname, 'post_install.sh')
        env = os.environ
        if 'PIP' not in env:
            env['PIP'] = self.get_pip()
        env['GIT_DIR'] = self.dirname
        env['NAME'] = self.name
        env['VIM_ENV'] = join(self.home, '.vim', 'ohmyvim', 'env.vim')
        if isfile(script):
            self.log('Running post install script...')
            os.chdir(self.dirname)
            p = Popen([script], env=env)
            p.wait()

    def self_upgrade(self):
        """Try to upgrade itself"""
        branch = "master"
        with open(join(self.home, '.vimrc')) as fd:
            for line in fd:
                line = line.strip()
                if not line.startswith('"'):
                    if 'ohmyvim_skip_upgrade' in line and '=' in line:
                        if int(line.split('=', 1)[1].strip()):
                            line = line.replace('let', '').strip()
                            self.log('Skipping. vimrc contains %s' % line)
                            return
                    elif 'ohmyvim_version' in line:
                        branch = line.split('=').strip()

        if 'BUILDOUT_ORIGINAL_PYTHONPATH' in os.environ:
            self.log('Update your buildout')
            return False

        pip = self.get_pip()

        if pip:
            install_dir = join(self.home, '.oh-my-vim/')
            if os.path.isdir(install_dir):
                bin_dir = join(install_dir, 'env', 'bin')
            else:
                bin_dir = os.path.dirname(sys.executable)
                install_dir = None

            cmd = [pip, 'install', '-q',
                   '--src=%s' % join(self.home, '.vim', 'bundle')]

            if install_dir:
                bin_dir = join(install_dir, 'bin')
                cmd.append(('--install-option='
                            '--script-dir==%s') % bin_dir)

            cmd.extend(['-e',
                        'git+%s@%s#egg=oh-my-vim' % (self.remote, branch)])

            if self.home not in cmd[0]:
                cmd.insert(0, 'sudo')

            self.log('Upgrading to %s' % branch)
            if '__ohmyvim_test__' in os.environ:
                self.log(' '.join(cmd))
                return True
            else:
                p = Popen(cmd)
                p.wait()
                return True

        os.chdir(self.dirname)
        p = Popen(['git', 'pull', '-qn', 'origin', branch], stdout=PIPE)
        p.wait()

        self.log("! Dont know how to upgrade oh-my-vim's python package...")
        self.log('! You may try to update it manualy')


class Manager(object):

    dependencies = {
        'vim-pathogen': 'https://github.com/tpope/vim-pathogen.git',
        'oh-my-vim': GIT_URL,
    }

    def __init__(self):
        self.output = []

        self.home = os.environ['HOME']
        self.vim = join(self.home, '.vim')
        self.vimrc = join(self.home, '.vimrc')
        self.gvimrc = join(self.home, '.gvimrc')
        self.runtime = join(self.vim, 'bundle')
        self.autoload = join(self.vim, 'autoload')
        self.ohmyvim = join(self.vim, 'ohmyvim')

        for dirname in (self.runtime, self.autoload,
                        self.ohmyvim):
            if not isdir(dirname):
                os.makedirs(dirname)

        for name, url in self.dependencies.items():
            if not isdir(join(self.runtime, name)):
                self.log('Installing %s...' % name)
                Popen(['git', 'clone', '-q', url,
                       join(self.runtime, name)]).wait()

        if not isfile(join(self.ohmyvim, 'theme.vim')):
            with open(join(self.ohmyvim, 'theme.vim'), 'w') as fd:
                fd.write('')

        if not isfile(join(self.ohmyvim, 'env.vim')):
            with open(join(self.ohmyvim, 'env.vim'), 'w') as fd:
                fd.write('set path+=$HOME/.oh-my-vim/bin\n')

        ohmyvim = join(self.ohmyvim, 'ohmyvim.vim')
        with open(ohmyvim, 'w') as fd:
            fd.write('source %s\n' % join(self.ohmyvim, 'env.vim'))
            fd.write('source %s\n' % join(self.runtime, 'vim-pathogen',
                                          'autoload', 'pathogen.vim'))
            fd.write("call pathogen#infect('bundle/{}')\n")
            fd.write('source %s\n' % join(self.ohmyvim, 'theme.vim'))
            fd.write('source %s\n' % join(self.runtime, 'oh-my-vim',
                                          'plugin', 'ohmyvim.vim'))

        if 'VIRTUAL_ENV' in os.environ:
            binary = join(os.getenv('VIRTUAL_ENV'), 'bin', 'oh-my-vim')
        else:
            binary = 'oh-my-vim'

        need_update = False
        if not isfile(self.vimrc):
            need_update = True
        else:
            with open(self.vimrc) as fd:
                if ohmyvim not in fd.read():
                    need_update = True

        if need_update:
            if isfile(self.vimrc):
                with open(self.vimrc, 'r') as fd:
                    data = fd.read()
                with open(join(self.ohmyvim, 'vimrc.bak'), 'w') as fd:
                    fd.write(data)
            else:
                data = ''
            kw = dict(
                ohmyvim=ohmyvim,
                binary=binary,
                profiles=self.profiles(None, as_list=True))
            with open(self.vimrc, 'w') as fd:
                fd.write(VIMRC % kw)
                fd.write(data)

        if not isfile(self.gvimrc):
            with open(self.gvimrc, 'w') as fd:
                fd.write(GVIMRC)

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
               "type=Repositories&l=Vim&q=") + terms
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
            printed = set()
            bundles = config.bundles.items() + config.vimscripts.items()
            for name, url in bundles:
                if name not in printed:
                    printed.add(name)
                    if args.raw:
                        self.log(name)
                    else:
                        self.log('- %s (%s)', name, url)

    def install(self, args):
        config = get_config()
        requires = join(TOOLS, 'requires')
        if args.raw:
            if args.dist:
                for require in glob(join(requires, '*.txt')):
                    name = basename(require)[:-4]
                    if name != 'gawel':
                        self.log(name)
            else:
                for name in sorted(config.bundles.keys()):
                    self.log(name)
                for name in sorted(config.vimscripts.keys()):
                    self.log(name)
        else:
            if args.dist:
                if not isinstance(args.url, list):
                    args.url = []
                args.url.append(join(requires, '%s.txt' % args.dist))

            dependencies = set()
            for url in args.url:
                if url.endswith('.txt'):
                    if isfile(url):
                        with open(url) as fd:
                            for dep in fd:
                                dep = dep.strip()
                                if dep and not dep.startswith('#'):
                                    dependencies.add(dep)
                    elif url.startswith('http'):
                        fd = urlopen(url)
                        for dep in fd.readlines():
                            dep = dep.strip()
                            if dep and not dep.startswith('#'):
                                dependencies.add(dep)
                else:
                    b = Bundle.install(self, args, url)
                    if b:
                        dependencies = dependencies.union(b.dependencies)
            if dependencies:
                self.log('Processing dependencies...')
                for url in dependencies:
                    if url.strip():
                        b = Bundle.install(self, args, url.strip())

    def upgrade(self, args):
        for b in self.get_bundles():
            if b.name in args.bundle or len(args.bundle) == 0:
                b.upgrade(args)

    def remove(self, args):
        if args.bundle:
            bundles = [b.lower() for b in args.bundle]
            for b in self.get_bundles():
                if b.name.lower() in bundles:
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

    def profiles(self, args, as_list=False):
        profiles = join(self.runtime, 'oh-my-vim', 'profiles')
        profiles = glob(join(profiles, '*.vim'))

        if as_list:
            return sorted([basename(name)[:-4] for name in profiles])

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

    def version(self, args):
        version = pkg_resources.get_distribution('oh-my-vim').version
        self.log(version)


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
    p.add_argument('-f', '--full', default=None,
                   help="also install required softwares and binaries")
    p.add_argument('-d', '--dist', default=None,
                   help="install a distribution")
    p.add_argument('url', nargs='*', default='')
    p.set_defaults(action=manager.install)

    p = subparsers.add_parser('upgrade', help='upgrade bundles')
    p.add_argument('-f', '--full', default=None,
                   help="also install required softwares and binaries")
    p.add_argument('bundle', nargs='*', default='')
    p.set_defaults(action=manager.upgrade)

    p = subparsers.add_parser('remove', help='remove a bundle')
    p.add_argument('bundle', nargs='*', default='')
    p.set_defaults(action=manager.remove)

    p = subparsers.add_parser('theme', help='list or activate a theme')
    p.add_argument('--raw', action='store_true', default=False)
    p.add_argument('theme', nargs='?', default='')
    p.set_defaults(action=manager.theme)

    p = subparsers.add_parser('profiles', help='print all available profiles')
    p.set_defaults(action=manager.profiles)

    p = subparsers.add_parser('version', help='print version')
    p.set_defaults(action=manager.version)

    if args:
        args = parser.parse_args(args)
    else:
        args = parser.parse_args()

    try:
        args.action(args)
    except AttributeError:
        parser.parse_args(['-h'])

    if '__ohmyvim_test__' in os.environ:
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
