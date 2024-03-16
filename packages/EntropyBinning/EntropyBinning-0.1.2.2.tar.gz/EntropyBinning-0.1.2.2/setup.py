from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.2.2'
DESCRIPTION = 'Entropy base binning for data analysis'

# Setting up
setup(
    name="EntropyBinning",
    version=VERSION,
    author="chingDev.Official (Prince Carl Ajoc)",
    author_email="chingace471@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy", "pandas"],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)