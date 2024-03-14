# Copyright (C) 2024 Matthias Nadig

from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

path_package_toplevel = 'src'

# PyTorch should be installed separately, as there are sometimes issues with the installation
install_requires = [
    'tacotree',
]

setup(
    name='tacotree_lab',
    version='1.0.0',
    description='Extension of tacotree toolbox',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matthias Nadig',
    author_email='nadig_develop@yahoo.com',
    license='MIT',
    package_dir={'': path_package_toplevel},
    packages=find_packages(where=path_package_toplevel),
    install_requires=install_requires,
)
