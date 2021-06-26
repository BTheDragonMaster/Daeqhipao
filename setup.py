from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Daeqhipao'
LONG_DESCRIPTION = 'A computer interface to play the Game of Gods.'

setup(
    name="daeqhipao",
    version=VERSION,
    author="Barbara Terlouw",
    author_email="barbara.r.terlouw@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={"": ["*.png"]},
    install_requires=[],
    scripts=["bin/daeqhipao"],
)