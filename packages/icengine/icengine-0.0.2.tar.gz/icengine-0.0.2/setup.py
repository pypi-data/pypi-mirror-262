from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'A Visual Game Engine For Python'
LONG_DESCRIPTION = 'A Visual Game Engine For Python Made To Stand Out Compared To Pygame And Pyglet, Plus Its Open Source: https://github.com/IAmDazen/Icengine'

# Setting up
setup(
    name="icengine",
    version=VERSION,
    author="Metaldev",
    author_email="<theducktalkshow@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'game engine'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
