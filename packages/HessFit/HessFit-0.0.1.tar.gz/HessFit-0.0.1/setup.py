from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'A package that allows to derive force field.'

# Setting up
setup(
    name="HessFit",
    version=VERSION,
    author="Emanuele Falbo",
    author_email="<falbo.emanuele@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
