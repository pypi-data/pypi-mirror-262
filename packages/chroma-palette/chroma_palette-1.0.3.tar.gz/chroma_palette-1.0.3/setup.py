from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.3'
DESCRIPTION = 'Chroma Palette - Text Styling Library'

# Setting up
setup(
    name="chroma_palette",
    version=VERSION,
    author="VK_Billava (Vinay Kumar)",
    author_email="<vinaykumarbillava@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'terminal', 'color', 'palette', 'color palette', 'termina palette', 'terminal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)