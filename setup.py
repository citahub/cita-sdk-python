#!/usr/bin/env python

"""The setup script."""
import importlib
from setuptools import setup

readme = ''
changes = ''

setup_requires = []
install_requires = [
    'requests==2.22.0',
    'eth-abi==2.1.0',
    'pysha3==1.0.2',
    'ecdsa==0.15',
    'secp256k1==0.13.2',
    'protobuf==3.11.3'
]

# Get the requirements list
with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()


module_name = 'pycita'
mod = importlib.import_module(module_name)


setup(
    name=mod.__name__,
    version=mod.__version__,
    description=mod.__description__,
    long_description=u"\n\n".join([readme, changes]),
    classifiers=[
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='nameko rpc',

    author=mod.__author__,
    author_email=mod.__email__,
    url=mod.__url__,

    packages=['pycita'],
    package_dir={'': 'src'},  # tell distutils packages are under src
    python_requires='>=3.6, <4',
    setup_requires=setup_requires,
    install_requires=install_requires,

    include_package_data=True,  # automatically include any data files it finds inside your package directories that are specified by your MANIFEST.in file
    zip_safe=False,  # this project CANNOT be safely installed and run from a zip file
)
