#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Command
from pip.req import parse_requirements
from pip.download import PipSession
from glob import glob

import os
import sys

PATH_ROOT = os.getcwd()


class MakeDoc(Command):
    """
    MakeDoc will prepare Python and JavaScript document from code.

    """
    description = "Prepares documentation"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """

        :return:
        """
        import sh

        env = os.environ.copy()

        # update RST files from python files
        sh.cd(os.path.join(PATH_ROOT, 'docs'))
        out = sh.sphinx_apidoc('-o', '.', '../fludashboard', '--force')
        print(out)

        # update RST files from python javascript files
        path_template = list(
            sh.grep(sh.locate('jsdoc-sphinx'), 'template$')
        )[0].replace('\n', '')

        out = sh.jsdoc(
            '-t', path_template, '-d', 'jsdoc/', '../fludashboard/static/js/'
        )
        print(out)



def list_dir(pathname=PATH_ROOT, dir_name=''):
    result = glob(
        os.path.join(pathname, dir_name, '**'), 
        recursive=True
    )[1:]

    size = len(pathname)

    return ['.%s' % r[size:] for r in result]

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
    cmdclass={'doc': MakeDoc},
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
