#!/usr/bin/env python

import setuptools

setuptools.setup(use_scm_version=True,
                 packages=setuptools.find_packages(exclude=['docs', 'tests']), )
