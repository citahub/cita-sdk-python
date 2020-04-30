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


module_name = 'cita'
mod = importlib.import_module(module_name)


setup(
    name='cita_sdk_python',
    version=mod.__version__,
    description=mod.__description__,
    long_description=u"\n\n".join([readme, changes]),
    platforms=['Windows', 'Mac OS-X', 'Linux', 'Unix'],
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'License :: OSI Approved :: Apache License, Version 2.0 (Apache-2.0)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='cita blockchain',

    author=mod.__author__,
    author_email=mod.__email__,
    url=mod.__url__,

    packages=['cita'],
    package_dir={'': 'src'},  # tell distutils packages are under src
    python_requires='>=3.7, <4',
    setup_requires=setup_requires,
    install_requires=install_requires,

    include_package_data=True,  # automatically include any data files it finds inside your package directories that are specified by your MANIFEST.in file
    zip_safe=False,  # this project CANNOT be safely installed and run from a zip file
)
