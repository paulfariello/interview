#!/usr/bin/env python3

import os
import glob
import subprocess

from distutils.core import setup
from setuptools.command.sdist import sdist


class SdistCommand(sdist):
    def run(self):
        #subprocess.check_call(['npm', 'install'], cwd='client')
        #subprocess.check_call(['node', 'build/build.js'], cwd='client')
        super().run()


setup(name='Interview',
      version='1.0',
      description='Web interview',
      author='Paul Fariello',
      author_email='paul@fariello.eu',
      url='https://github.com/paulfariello/Interview',
      packages=['itw'],
      classifiers=['Environment :: Web Environment',
                   'Intended Audience :: End Users/Desktop',
                   'Operating System :: POSIX',
                   'Programming Language :: Python',
                   'Programming Language :: Javascript'],
      cmdclass={'sdist': SdistCommand})
