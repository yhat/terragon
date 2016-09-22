from distutils.core import setup
from setuptools import find_packages


required = []

setup(
    name="terragon",
    version="0.3.0",
    author="Greg Lamp",
    author_email="greg@yhathq.com",
    url="https://github.com/yhat/terragon/",
    license="BSD",
    packages=find_packages(),
    description="a better pickle",
    long_description="why is it so hard to reference a file in your setup.py?",
    install_requires=required,
)
