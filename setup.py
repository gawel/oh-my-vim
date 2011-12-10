from setuptools import setup, find_packages
import sys, os

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
