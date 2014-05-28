#!/usr/bin/env python

from distutils.core import setup

setup(name='ace',
      version='0.0.1',
      description='Ethereum contract development environment',
      author='Rob Myers',
      author_email='rob@robmyers.org',
      packages=['ace'],
      package_data={'ace': ['files/config/*.yaml',
                            'files/serpent/*.se',
                            'files/test/*.py.template']},
      scripts=['scripts/ace']
     )
