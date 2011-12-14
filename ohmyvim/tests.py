# -*- coding: utf-8 -*-
import unittest2 as unittest
from ohmyvim.scripts import main
from os.path import isdir
from os.path import isfile
from os.path import join
import subprocess
import tempfile
import shutil
import os


class Mixin(object):

    def setUpMixin(self):
        self.addCleanup(os.chdir, os.getcwd())
        self.wd = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.wd)
        os.environ['HOME'] = self.wd

    def assertIsFile(self, *args):
        filename = join(self.wd, *args)
        if not isfile(filename):
            print(os.listdir(os.path.dirname(filename)))
            self.assertTrue(isfile(filename), filename)

    def assertIsDir(self, *args):
        dirname = join(self.wd, *args)
        if not isdir(dirname):
            print(os.listdir(os.path.dirname(dirname)))
            self.assertTrue(isfile(dirname), dirname)

    def assertResp(self, resp):
        self.assertTrue(len(resp) > 0, resp)


class TestScript(unittest.TestCase, Mixin):

    def setUp(self):
        self.setUpMixin()
        os.environ['__ohmyvim_test__'] = '1'
        self.requires = join(self.wd, 'deps.txt')
        with open(self.requires, 'w') as fd:
            fd.write('https://github.com/vim-scripts/github-theme.git\n\n')

    def main(self, args):
        return main(*args.split(' '))

    def test_ohmyvim(self):
        self.main('install')
        self.assertIn(self.wd, os.path.expanduser('~/'))
        self.assertIsFile('.vim/ohmyvim/ohmyvim.vim')
        self.assertIsDir('.vim/bundle/oh-my-vim')

        url = self.main('search')[0]
        self.assertIn('language%3AVimL', url)

        url = self.main('search -t')[0]
        self.assertIn('colorschemes', url)

        url = self.main('search -t mytheme')[0]
        self.assertIn('colorschemes', url)
        self.assertIn('mytheme', url)

        resp = self.main('profiles')
        self.assertIn('* defaults - some defaults settings', resp)

        resp = self.main('install --raw')
        self.assertIn('github-theme', resp)

        self.main('install')
        resp = self.main('install github-theme')
        self.assertResp(resp)

        resp = self.main(
                'install https://github.com/vim-scripts/github-theme.git')
        self.assertIn('github-theme already installed.', resp)

        resp = self.main('install %s' % self.requires)
        self.assertIn('github-theme already installed.', resp)

        resp = self.main(
                'install scrooloose/nerdtree')
        self.assertIn('Installing nerdtree...', resp)

        resp = self.main(
                'install hg+https://bitbucket.org/sjl/gundo.vim')
        self.assertIn('Installing gundo.vim...', resp)

        resp = self.main('list --raw')
        self.assertIn('github-theme', resp)
        self.assertIn('gundo.vim', resp)

        resp = self.main('list')
        self.assertIn(
           '* github-theme (https://github.com/vim-scripts/github-theme.git)',
           resp)

        resp = self.main('list -u')
        self.assertIn('git+https://github.com/vim-scripts/github-theme.git',
                      resp)

        resp = self.main('theme --raw')
        self.assertIn('github', resp)

        resp = self.main('theme')
        self.assertIn('\t- github', resp)

        resp = self.main('theme github')
        self.assertIn('Activate github theme...', resp)

        resp = self.main('remove')
        self.assertTrue(len(resp) == 0)

        resp = self.main('remove github-theme')
        self.assertNotIn('github-theme', resp)

        resp = self.main('upgrade oh-my-vim')
        self.assertIn('Upgrading oh-my-vim...', resp)

        resp = self.main('info vim-IPython')
        self.assertIn('https://github.com/vim-scripts/vim-ipython#readme',
                      resp)


class TestInstall(unittest.TestCase, Mixin):

    def setUp(self):
        self.setUpMixin()

        def setenv(key, value):
            os.environ[key] = value

        self.addCleanup(setenv, 'PYTHONPATH', os.environ['PYTHONPATH'])
        self.addCleanup(setenv, 'BUILDOUT_ORIGINAL_PYTHONPATH',
                                os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'])
        os.environ['PYTHONPATH'] = ''
        del os.environ['BUILDOUT_ORIGINAL_PYTHONPATH']

    def test_install(self):
        script = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'tools', 'install.sh')
        subprocess.Popen('sh %s' % script, shell=True).wait()
        self.assertIsFile('.oh-my-vim/env/bin/python')
        self.assertIsFile('.oh-my-vim/bin/oh-my-vim')
        subprocess.Popen(' '.join(
                       [os.path.join(self.wd, '.oh-my-vim/bin/oh-my-vim'),
                       'upgrade']),
                       shell=True).wait()
