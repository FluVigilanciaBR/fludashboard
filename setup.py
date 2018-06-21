#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Command
from pip.req import parse_requirements
from pip.download import PipSession

import os

PATH_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_version():
    """Obtain the version number"""
    import importlib
    mod = importlib.machinery.SourceFileLoader(
        'version', os.path.join('fludashboard', '__init__.py')
    ).load_module()
    return mod.__version__


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
    version=get_version(),
    description="Flu Dashboard",
    long_description=readme + '\n\n' + history,
    author="Marcelo F C Gomes, Ivan Ogasawara",
    author_email='marcelo.gomes@fiocruz.br, ivan.ogasawara@gmail.com',
    url='https://github.com/FluVigilanciaBR/fludashboard',
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
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='fludashboard',
    classifiers=[
        'Development Status :: 4 - Beta',
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
