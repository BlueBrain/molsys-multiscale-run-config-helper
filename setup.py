#!/usr/bin/env python

import importlib.util

from setuptools import find_packages, setup

spec = importlib.util.spec_from_file_location("multiscale_run_config_helper.version", "multiscale_run_config_helper/version.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
VERSION = module.VERSION


setup(
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    name="multiscale_run_config_helper",
    version=VERSION,
    description="multiscale_run configurqtion files generator",
    author="Jean Jacquemier",
    author_email="jean.jacquemier@epfl.ch",
    url="https://bbpgitlab.epfl.ch/molsys/multiscale_run_config_helper",
    project_urls={
        "Tracker": "",
        "Source": "git@bbpgitlab.epfl.ch:molsys/multiscale_run_config_helper.git",
    },
    license="BBP-internal-confidential",
    install_requires=[
        "bluepysnap>=1.0.7",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
    ],
    extras_require={},
    packages=find_packages(),
    scripts=[],
    include_package_data=True,
)
