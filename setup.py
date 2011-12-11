from setuptools import setup, find_packages
import sys, os

if os.getuid() == 0:
    sys.stderr.write('Please do not install me as root!\n')
    sys.exit(-1)

version = '0.1'

def read(*args):
    path = os.path.join(*args)
    try:
        return open(path).read()
    except:
        pass
    return ''

setup(name='oh-my-vim',
      version=version,
      description="Vim manager",
      long_description=read('README.rst'),
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Topic :: Software Development',
          'Topic :: Text Editors',
          ],
      keywords='vim pathogen',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='https://github.com/gawel/oh-my-vim',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'argparse',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      oh-my-vim = ohmyvim.scripts:main
      """,
      )

def upgrade():
    sys.path.insert(0, os.path.dirname(__file__))
    class Args(object):
        def __init__(self, dependencies):
            self.bundle = dependencies
    try:
        from ohmyvim.scripts import Manager
        manager = Manager()
        manager.upgrade(Args(manager.dependencies.keys()))
    except Exception:
        sys.stderr.write('Auto upgrade failed. Please run:\n')
        sys.stderr.write('    $ oh-my-vim upgrade\n')

if 'install' in sys.argv or 'bdist_egg' in sys.argv:
    upgrade()
