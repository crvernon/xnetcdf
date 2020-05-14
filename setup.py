"""Setup file for <your model name>

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().split()


setup(
    name='xnetcdf',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/crvernon/xnetcdf.git',
    license='BSD 2-Clause',
    author='Chris R. Vernon, Casey McGrath',
    author_email='chris.vernon@pnnl.gov, casey.mcgrath@pnnl.gov',
    description='NetCDF builder for Xanthos standard outputs',
    python_requires='>=3.3.*, <4'
)
