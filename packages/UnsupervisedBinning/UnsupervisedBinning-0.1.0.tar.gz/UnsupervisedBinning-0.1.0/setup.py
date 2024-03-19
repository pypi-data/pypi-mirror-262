from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.0'
DESCRIPTION = 'Unsupervised Analysis Binning'

# Setting up
setup(
    name="UnsupervisedBinning",
    version=VERSION,
    author="chingDev.Official (Prince Carl Ajoc)",
    author_email="chingace471@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['unsupervised learning', 'binning', 'data analysis', 'machine learning', 'clustering', 'data science'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)