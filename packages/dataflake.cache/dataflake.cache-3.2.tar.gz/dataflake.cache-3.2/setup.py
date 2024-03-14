##############################################################################
#
# Copyright (c) 2009-2023 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(name='dataflake.cache',
      version='3.2',
      description='Simple caching library',
      long_description=read('README.rst'),
      long_description_content_type='text/x-rst',
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='cache',
      author="Jens Vagelpohl and contributors",
      author_email="jens@dataflake.org",
      url='https://github.com/dataflake/dataflake.cache',
      project_urls={
        'Documentation': 'https://dataflakecache.readthedocs.io',
        'Sources': 'https://github.com/dataflake/dataflake.cache',
        'Issue Tracker': 'https://github.com/dataflake/dataflake.cache/issues',
      },
      license="ZPL 2.1",
      package_dir={'': 'src'},
      packages=['dataflake.cache'],
      python_requires='>=3.7',
      include_package_data=True,
      install_requires=[
        'setuptools',
        'zope.interface',
        ],
      extras_require={
        'docs': ['Sphinx',
                 'repoze.sphinx.autointerface',
                 'sphinx_rtd_theme',
                 'pkginfo',
                 ],
        },
      tests_require=[
        'zope.testing',
        'zope.testrunner',
        ],
      zip_safe=False,
      test_suite='dataflake.cache.tests',
      )
