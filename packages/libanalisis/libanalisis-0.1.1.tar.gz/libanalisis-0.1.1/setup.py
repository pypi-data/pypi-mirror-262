# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 11:40:26 2024

@author: HOME
"""

from setuptools import setup, find_packages

setup(
    name='libanalisis',
    version='0.1.1',
    author='Orlando Arroyo',
    author_email='odarroyo@uc.cl',
    packages=find_packages(),
    description='A collection of OpenSeesPy routines for performing several types of analyses',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'openseespy>=3.5',  # Requires a version of OpenSeesPy later than 3.9
        'matplotlib',  # Any version of matplotlib
        'numpy',  # Any version of numpy
    ],
    python_requires='>=3.9', # Adjust based on your compatibility
    url='https://github.com/odarroyo/libanalisis',
    license='LICENSE', # If you have a license file
)