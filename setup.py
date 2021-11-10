from distutils.core import setup
import setuptools
import os

requires = ['scipy', 'jinja2']
version = 0.1

packages = ['blockmeshdictator']

root_dir = os.path.dirname(__file__)
setup(
    name='blockmeshdictator',
    version=version,
    packages=packages,
    package_dir={'blockmeshdictator': 'blockmeshdictator'},
    license='GPL-v3',
    requires=requires,
    author='Booya',
    url='www.openglider.org'
)

