from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

ext_modules = [
    Extension("sandData",
              ["sandData.pyx"],
              include_dirs=[np.get_include()]), 
    Extension("update",
              ["update.pyx"],
              include_dirs=[np.get_include()])
]

setup(
    name='Fluent Python',
    ext_modules=cythonize(ext_modules),
)