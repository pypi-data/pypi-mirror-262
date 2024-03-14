# Copyright (C) 2024 Matthias Nadig

from setuptools import setup, find_packages
import warnings


with open('README.md', 'r') as f:
    long_description = f.read()

path_package_toplevel = 'src'

# Minimal Python version
# (3.7 is required for breakpoint function)
python_requires = '>=3.7'

# Required PyTorch packages
pytorch_packages = [
    'torch',
    'torchvision',
]

# PyTorch should be installed separately, as there are sometimes issues with the installation
install_requires = [
    'tacotree_lab',
    'numpy',
    'ndbounds',
    *pytorch_packages,
]

# Check if PyTorch has already been installed separately
missing_packages = []
for package in pytorch_packages:
    # Make sure that package name contains nothing but ASCII and alphanumeric characters
    if not all([char.isascii() and char.isalnum() for char in package]):
        str_e = f'Package name has unexpected characters: "{package}"'
        raise RuntimeError(str_e)

    # Import the package test-wise to see if it is there
    try:
        exec(f'import {package}')
    except ImportError:
        missing_packages.append(package)

# Throw error if any PyTorch package is not available
if len(missing_packages) > 0:
    str_e = (
        'At least one PyTorch package is missing. ' +
        'PyTorch should be installed separately from tacotree, as its installation ' +
        'can sometimes be tricky and hardware-dependent. ' +
        'Following packages are missing:' +
        ('\n\t* {}' * len(missing_packages)).format(*missing_packages)
    )
    warnings.warn(str_e)

setup(
    name='tacotree',
    version='1.0.0',
    description='Data processing pipelines based on PyTorch',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matthias Nadig',
    author_email='nadig_develop@yahoo.com',
    license='MIT',
    package_dir={'': path_package_toplevel},
    packages=find_packages(where=path_package_toplevel),
    python_requires=python_requires,
    install_requires=install_requires,
)
