from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A package that allows to derive force field.'

# Setting up
setup(
    name="HessFit",
    version=VERSION,
    author="Emanuele Falbo",
    author_email="falbo.emanuele@gmail.com",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/emanuelefalbo/HessFit", 
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['numpy', 'pandas'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['HessFit = HessFit.main:main']
    }
)

