#!/usr/bin/env python
from setuptools import setup

setup(
    name="ladock",
    version="0.1.6",
    description="LADOCK is an innovative and free tool designed for conducting simultaneous simulations in computer-aided drug discovery, encompassing molecular docking and molecular dynamics. In molecular docking, LADOCK excels in handling single or double ligands. It supports ligands from various online sources. In molecular dynamics, LADOCK efficiently manages protein-ligand interactions and even ligand-ligand interactions, accommodating scenarios with one or multiple proteins and ligands.",
    author="La Ode Aman",
    author_email="laode_aman@ung.ac.id",
    license="Apache License 2.0",
    packages=["ladock"],
    python_requires='>=3.9',    
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ladockgui=ladock.gui:main',
            'ladock=ladock.nogui:main'
        ],
    },
)
