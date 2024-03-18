from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Check EVM wallet balance with GUI'

# Setting up
setup(
    name="zeleva",
    version=VERSION,
    author="Mamang Joko",
    author_email="aimar.airdrop123@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['zuperscripts', 'tkinter'],
    keywords=['python', 'interface'],
    license="MIT",
    url="https://github.com/0xraia/zeleva.git",
    project_urls={
        'Source': 'https://github.com/0xraia/zeleva.git',
    },
)
