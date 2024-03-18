# Copyright 2024 ETH Zurich and University of Bologna.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0
#
# Author: Luca Colagrande <colluca@iis.ee.ethz.ch>
from setuptools import setup, find_packages
import cmake_build_extension
from pathlib import Path

setup(
	packages=find_packages(),
	setup_requires=['cffi'],
	install_requires=['cffi'],
	cffi_modules=["pyflexfloat/build_flexfloat_ffi.py:ffibuilder"],
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="ToFind",
            install_prefix="pyflexfloat",
            source_dir=str(Path(__file__).parent.absolute() / 'flexfloat')
        )
    ],
    cmdclass=dict(
        build_ext=cmake_build_extension.BuildExtension,
    )
)
