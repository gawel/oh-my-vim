from setuptools import setup, find_packages
import os

version = '0.6'


def read(*args):
    path = os.path.join(*args)
    try:
        return open(path).read()
    except:
        pass
    return ''

setup(name='oh-my-vim',
      version=version,
      description="Vim plugin manager and Vim related stuff",
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
          'ConfigObject',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      oh-my-vim = ohmyvim.scripts:main
      fpcli = ohmyvim.fpcli:main
      """,
      )
