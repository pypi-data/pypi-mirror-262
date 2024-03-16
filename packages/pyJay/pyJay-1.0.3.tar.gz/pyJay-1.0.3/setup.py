from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.3'
DESCRIPTION = 'Develop games easier'
LONG_DESCRIPTION = 'PyJay is a module that acts like a game engine for Pygame. Define buttons, animations, and more. View the documentation at connorlayson.github.io/pyJay'

# Setting up
setup(
    name="pyJay",
    version=VERSION,
    author="Connor Layson",
    author_email="<clayson2573@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'pygame', 'game'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
