# python setup.py develop
from setuptools import setup, find_packages
setup(
    name='zhr_demo',
    version='0.1.0',
    author='zaoheren',
    description='demo',
    author_email='zaoheren@hotmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
)