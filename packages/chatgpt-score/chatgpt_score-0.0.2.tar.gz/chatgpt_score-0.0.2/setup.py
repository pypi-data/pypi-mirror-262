#!/usr/bin/env python
from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from expviz.version import __version__

setup(
    name='chatgpt_score',
    version=__version__,
    description='',
    url='https://github.com/fuzihaofzh/chatgpt_score',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    keywords='Shell env',
    packages=find_packages(),
    install_requires=["openai"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)