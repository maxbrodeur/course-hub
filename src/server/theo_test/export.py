from setuptools import setup
from Cython.Build import cythonize
from os import path

this_dir = path.dirname(path.realpath(__file__))

setup(ext_modules = cythonize(
	this_dir+"/*.pyx",
	language="c++"
	))