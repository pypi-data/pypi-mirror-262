# python setup.py develop
from setuptools import setup, find_packages
setup(
    name='zaoheren_utils',
    version='0.1.0',
    author='zaoheren',
    description='A small example package',
    author_email='zaoheren@hotmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
)