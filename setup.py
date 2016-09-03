#!/usr/bin/env python

import os
import sys

import escea

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'escea'
]

requires = [
]
tests_require=[
]

with open('LICENSE') as f:
    license = f.read()

setup(
    name=escea.__title__,
    version=escea.__version__,
    description='Escea Fireplace API Client',
    long_description='Escea Fireplace API Client',
    author='Mal Curtis',
    author_email='mal@mal.co.nz',
    url='http://mal.co.nz',
    packages=packages,
	tests_require=tests_require,
	test_suite='escea.tests',
    install_requires=requires,
    license=license,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',

    ),
)
