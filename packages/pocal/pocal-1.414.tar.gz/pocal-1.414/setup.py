import setuptools
from setuptools import find_packages, setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pocal",
    version = "1.414",
    description = "POCAL (Python Optical Coating Analysis Library)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages(),
    py_modules=['thinfilms','__init__'],
    classifiers = [
        "Programming Language :: Python"
    ]
)