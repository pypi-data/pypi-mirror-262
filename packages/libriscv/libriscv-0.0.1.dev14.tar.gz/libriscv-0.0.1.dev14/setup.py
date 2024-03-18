#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
from setuptools import setup
# pylint: disable=import-error
from pybind11.setup_helpers import Pybind11Extension, build_ext

RISCV = os.environ.get("RISCV", "/opt/riscv")

mod = Pybind11Extension(
    "libriscv._riscv",
    glob.glob("src/main/cpp/*.cc"),
    define_macros=[
        ("NDEBUG", "1")
    ],
    extra_compile_args=[
        "-std=c++17",
    ],
    libraries=[
        "disasm",
    ],
    extra_link_args=[
        f"-Wl,-rpath,{RISCV}/lib",
        f"-L{RISCV}/lib",
    ],
    include_dirs=[
        "src/main/cpp",
        f"{RISCV}/include",
    ]
)

setup(
    ext_modules=[mod],
    cmdclass={"build_ext": build_ext}
)
