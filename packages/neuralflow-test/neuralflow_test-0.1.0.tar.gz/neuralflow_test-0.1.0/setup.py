from setuptools import setup, find_packages
setup(
name='neuralflow_test',
version='0.1.0',
author='Tanish Jain',
author_email='tanish.jdh2020@gmail.com',
description='A library which can load your deep learning code from text file as well as save it as a Keras model',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)