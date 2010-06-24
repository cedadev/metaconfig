# BSD Licence
# Copyright (c) 2010, Science & Technology Facilities Council (STFC)
# All rights reserved.
#
# See the LICENSE file in the source distribution of this software for
# the full license text.

from setuptools import setup, find_packages
import sys, os

__version__ = '0.1'

setup(name='metaconfig',
      version=__version__,
      description="A ConfigParser bootstraping library",
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
        ], 
      keywords='',
      author='Stephen Pascoe',
      author_email='Stephen.Pascoe@stfc.ac.uk',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points= {
        },
      test_suite='nose.collector',
      )
