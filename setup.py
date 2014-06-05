from distutils.core import setup
from setuptools import find_packages


required = []

setup(
    name="terragon",
    version="0.1.3",
    author="Greg Lamp",
    author_email="greg@yhathq.com",
    url="https://github.com/yhat/terragon/",
    license="BSD",
    packages=find_packages(),
    package_data={'': ['README.rst']},
    description="a better pickle",
    long_description=open("README.rst").read(),
    install_requires=required,
)

