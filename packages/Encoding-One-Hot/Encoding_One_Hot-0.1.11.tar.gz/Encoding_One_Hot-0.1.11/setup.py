from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.11'
DESCRIPTION = 'One hot encoding Categorical to Numerical'

# Setting up
setup(
    name="Encoding_One_Hot",
    version=VERSION,
    author="chingDev.Official (Prince Carl Ajoc)",
    author_email="chingace471@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['encoding', 'categorical data', 'numerical data', 'data preprocessing', 'machine learning', 'data science'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)