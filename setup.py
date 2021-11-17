from distutils.core import setup
import setuptools
import os

version = 0.1

packages = ['blockmeshdictator']

setup(
    name='blockmeshdictator',
    version=version,
    packages=packages,
    package_data={"blockmeshdictator": ["py.typed", "blockMeshDict", "blockMeshDict_whole", "new"]},
    package_dir={'blockmeshdictator': 'blockmeshdictator'},
    license='GPL-v3',
    requires=['scipy', 'jinja2'],
    author='Booya',
    url='www.openglider.org'
)

