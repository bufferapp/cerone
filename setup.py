# !/usr/bin/env python

from setuptools import setup

setup(
    name='cerone',
    packages=[],
    version='0.1.0',
    description='Extensible consumer made for applications using Python KCL.',
    author='David Gasquez',
    license='MIT',
    author_email='davidgasquez@buffer.com',
    url='https://github.com/bufferapp/cerone',
    keywords=['kcl', 'kinesis'],
    install_requires=['amazon_kclpy']
)
