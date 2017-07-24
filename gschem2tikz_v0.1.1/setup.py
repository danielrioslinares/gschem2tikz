#!/usr/bin/python

import os
from setuptools import setup

long_description = ("Convert gschem (gEDA) .sch schematic output files to "
	".tikz LaTeX tikzpicture files")

descrip = ("Tool for convert a gschem (gEDA) schematic to TikZ")

setup(
	name = "gschem2tikz",
	version = "0.1.0",
	author = "Daniel Ríos Linares",
	author_email = "riv@hotmail.es",
	description = descrip,
	license = "GPL",
	keywords = "gEDA, TikZ, LaTeX, python, circuitikz, diagram",
	long_description=long_description,
	packages = ['core','gui','cfg'],
	package_dir = {'core' : 'core', 'gui' : 'gui', 'cfg' : 'gui'},
	classifiers = [
		"Development Status :: 1 - Beta",
		"Environment :: GUI",
		"Intended Audience :: End Users/Desktop",
		"Topic :: Scientific/Engineering",
		"Topic :: Scientific/Engineering :: Physics",
		"License :: OSI Approved :: Python Software Foundation License",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: POSIX",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Topic :: Communications :: Email"
		],
)
