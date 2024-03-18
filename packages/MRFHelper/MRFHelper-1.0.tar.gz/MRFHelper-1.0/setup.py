from distutils.core import setup
from setuptools import find_packages

VERSION = '1.0'

setup(
      name='MRFHelper',
      version=VERSION,
      description='Generate tcl scripts of moment resisting frame for analysis using OpenSees',
      author='Wenchen Lie',
      author_email='438171766@qq.com',
      packages=find_packages()
)