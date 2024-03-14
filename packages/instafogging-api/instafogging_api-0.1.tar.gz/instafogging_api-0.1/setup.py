#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @description : description
# @file    : setup.py.py
# @author  : xingpeidong
# @email   : xpd1437@126.com
# @time    : 2024/3/14 15:31
"""
from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel

setup(
    name='instafogging_api',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        # Add other dependencies here
    ],
    test_suite='tests',
    tests_require=[
        'pytest',
        # Add other testing dependencies here
    ],
    author='xingpeidong',
    author_email='xpd1437@126.com',
    description='Description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/allesx/insta',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add other classifiers as needed
    ],
    cmdclass={'bdist_wheel': bdist_wheel},
)
