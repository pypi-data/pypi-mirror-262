# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 21:34:34 2023

@author: tjostmou
"""

from setuptools import setup, find_packages
from pathlib import Path


def get_version(rel_path):
    here = Path(__file__).parent.absolute()
    with open(here.joinpath(rel_path), "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="inflow-haisslab",
    version=get_version(Path("Inflow", "__init__.py")),
    packages=find_packages(),
    include_package_data=True,
    package_data={"Inflow.tiff": ["*.dll"]},
    url="https://gitlab.pasteur.fr/haisslab/analysis-packages/Inflow",
    license="MIT",
    author="Timothé Jost-MOUSSEAU",
    author_email="timothe.jost-mousseau@pasteur.com",
    description="General python code for analysis pipeline",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "cryptography>=38.0",
        "h5py>=3.7",
        "matplotlib>=3.6",
        "natsort>=8.2",
        "npTDMS>=1.6",
        "numpy>=1.23",
        "opencv_python_headless>=4.6",
        "pandas>=1.4",
        "paramiko>=2.8",
        "scipy>=1.9",
        "seaborn>=0.11",
        "suite2p",
        "concurrent-log-handler>=0.9",
        "timelined_array>=0.0.1",
    ],
    entry_points={},
    scripts=[],
)
