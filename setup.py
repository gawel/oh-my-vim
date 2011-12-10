from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='oh-my-vim',
      version=version,
      description="Vim manager",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='vim',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'restkit',
          'argparse',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      oh-my-vim = ohmyvim.scripts:main
      """,
      )
