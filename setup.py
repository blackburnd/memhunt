# -*- coding: utf-8 -*-
"""
This module contains the memhunt tool

"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    file_path = os.path.join(os.path.dirname(__file__), *rnames)
    with open(file_path, encoding='utf-8') as f:
        return f.read()


libname = 'memhunt'
libloc = [libname]
with open(os.path.join(*libloc+['version.txt']), encoding='utf-8') as f:
    version = f.read().strip()

long_description = (
    read('CHANGES.txt')
    + '\n' +
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    )

tests_require = [
    'pytest>=6.0',
    'pytest-cov>=2.10',
    'pytest-mock>=3.0',
]

setup(name='memhunt',
      version=version,
      description="Memory debugging tools for Python applications",
      long_description=long_description,
      long_description_content_type='text/plain',
      # Get more strings from https://pypi.org/classifiers/
      keywords="memory objgraph graphviz pympler debugging profiling",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Debuggers',
        'Topic :: System :: Monitoring'],
      author='Daniel Blackburn & Holmes Corporation',
      author_email='danielb@holmescorp.com',
      url="https://github.com/blackburnd/memhunt",
      license="ZPL 2.1",
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.8',
      install_requires=[
          'setuptools',
          'pympler>=0.9',
          'objgraph>=3.5.0',
          'jinja2>=3.0.0',
      ],
      tests_require=tests_require,
      extras_require={
          'tests': tests_require,
          'fastapi': [
              'fastapi>=0.68.0',
              'uvicorn>=0.15.0',
              'jinja2>=3.0.0',
          ],
          'dev': [
              'pytest>=6.0',
              'pytest-cov>=2.10',
              'pytest-mock>=3.0',
              'fastapi>=0.68.0',
              'uvicorn>=0.15.0',
          ],
      },
      test_suite='memhunt.tests.test_suite',
      )



      

