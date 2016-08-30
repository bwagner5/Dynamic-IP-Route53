#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Command

long_description = """
This utility updates a Route53 Zone with the public IP address of the computer it is running on.
"""

setup(
    name = 'update_ip',
    version = '1.0.0',
    license='MIT',
    description = 'Updates Route53 Zone with Public IP',
    long_description=long_description,
    author = 'Brandon Wagner',
    maintainer = 'Brandon Wagner',
    py_modules = [],
    scripts = ['update_ip.py'],
    zip_safe = True,
    install_requires=['boto3']
)
