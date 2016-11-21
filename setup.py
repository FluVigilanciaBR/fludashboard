#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession
from glob import glob

import os

PATH_ROOT = os.getcwd()


def list_dir(pathname=PATH_ROOT, dir_name=''):
    return glob(
        os.path.join(pathname, dir_name, '**'), 
        recursive=True
    )[1:]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

install_reqs = parse_requirements('requirements.txt', session=PipSession())

requirements = [str(ir.req) for ir in install_reqs]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='fludashboard',
    version='0.1.0',
    description="Flu Dashboard",
    long_description=readme + '\n\n' + history,
    author="Ivan Ogasawara",
    author_email='ivan.ogasawara@gmail.com',
    url='https://github.com/xmnlab/fludashboard',
    packages=[
        'fludashboard',
    ],
    package_dir={'fludashboard':
                 'fludashboard'},
    entry_points={
        'console_scripts': [
            'fludashboard=fludashboard.cli:main'
        ]
    },
    include_package_data=True,
    data_files=[
        ('data', list_dir(dir_name='data'))
    ],
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='fludashboard',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
