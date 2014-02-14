#!/usr/bin/env python

from setuptools import setup, find_packages

requires = ['psycopg2==2.5.1']

setup(name='pg_warmup',
      version          = '0.2.0',
      description      = 'PostgreSQL warmup tool',
      author           = 'Yoshiyuki Asaba',
      author_email     = 'ysyk.asaba@gmail.com',
      url              = 'https://github.com/y-asaba/pg_warmup',
      license          = "MIT License",
      packages         = find_packages(),
      install_requires = requires,
      classifiers  = [
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Database',
      ],
      entry_points = {
        'console_scripts': [ 'pg_warmup = pg_warmup.scripts.warmup:main' ],
      }
  )
