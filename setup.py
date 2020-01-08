#!/usr/bin/env python

import io
import re
import os
from setuptools import setup, find_packages


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', os.linesep)
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

def read_version():
    content = read(os.path.join(
        os.path.dirname(__file__), 'gurumcli', '__init__.py'))
    return re.search(r"__version__ = '([^']+)'", content).group(1)

setup(
    name='gurum-cli',
    version=read_version(),
    description='Gurum CLI is a tool to manage applications on the Gurum Platform.',
    long_description=read('README.md'),
    author='Karl Wallbom',
    author_email='wallbomk@amazon.com',
    url='https://github.com/kalleeh/gurum-cli',
    license=read('LICENSE'),
    packages=find_packages(exclude=('tests', 'docs')),
    keywords="Gurum CLI",
    # Support Python 2.7 and 3.6 or greater
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    entry_points={
        'console_scripts': [
            'gurum=gurumcli.cli.main:cli'
        ]
    },
    install_requires=[
        'boto3',
        'botocore',
        'click',
        'click-spinner',
        'colorama',
        'gitpython',
        'haikunator',
        'keyring',
        'prettytable',
        'termcolor',
        'yamale',
        'requests',
        'warrant'
    ],
    include_package_data=True
)
