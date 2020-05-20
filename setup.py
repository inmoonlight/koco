import os
from setuptools import find_packages, setup

REQ_FILE = 'requirements.txt'
VERSION = '0.2.2'


def get_requires():
    thisdir = os.path.dirname(__file__)
    reqpath = os.path.join(thisdir, REQ_FILE)
    return [line.rstrip('\n') for line in open(reqpath)]


setup(
    name='koco',
    version=VERSION,
    description='A library to easily access kocohub datasets',
    long_description=open('README.md', 'r', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Jihyung Moon',
    author_email='mjihyung@gmail.com',
    url='https://github.com/inmoonlight/koco',
    license='MIT',
    packages=find_packages(),
    install_requires=get_requires(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
    ],
    keywords='korean nlp datasets',
)
