from setuptools import setup, find_packages

setup(
name='ez-localizr',
version='0.0.1',
author='Tyler Koziol',
author_email='tora@tora-ouji.com',
description='An insanely simple localization tool for Python.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.8',
)