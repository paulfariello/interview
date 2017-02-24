#!/usr/bin/env python3

import os
import glob
import subprocess

from distutils.core import setup
from distutils.dist import Distribution
from distutils.command.build import build

build.sub_commands.append(('build_front', None))


class FrontDistribution(Distribution):
    def __init__(self, attrs=None):
        self.front = None
        super().__init__(attrs)


class BuildFrontCommand(build):
    def initialize_options(self):
        self.path = None

    def finalize_options(self):
        self.path = self.distribution.front

    def run(self):
        build.run(self)
        subprocess.check_call(['npm', 'install'], cwd=self.path)
        subprocess.check_call(['node', 'build/build.js'], cwd=self.path)

    sub_commands = []

if 'CLEVERCLOUD' in os.environ:
    # source /home/bas/.nvm/nvm.sh
    proc = subprocess.Popen(". /home/bas/.nvm/nvm.sh; env", shell=True, stdout=subprocess.PIPE)
    env, _ = proc.communicate()
    env = env.decode()
    env = env.splitlines()
    os.environ.update(dict([var.split("=", 1) for var in env]))

setup(name='Interview',
      version='1.0',
      description='Web interview',
      author='Paul Fariello',
      author_email='paul@fariello.eu',
      url='https://github.com/paulfariello/Interview',
      packages=['itw'],
      front='client',
      data_files=[('static', os.path.join('client', 'dist', 'index.html'))],
      classifiers=['Environment :: Web Environment',
                   'Intended Audience :: End Users/Desktop',
                   'Operating System :: POSIX',
                   'Programming Language :: Python',
                   'Programming Language :: Javascript'],
      distclass=FrontDistribution,
      cmdclass={'build_front': BuildFrontCommand})
