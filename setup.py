try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import gitsecrets

setup(name="python-git-secrets",
      version=python-git-secrets.__version__,
      description="Python implementation of git-secrets(https://github.com/awslabs/git-secrets)",
      long_description="Python implementation of git-secrets(https://github.com/awslabs/git-secrets)",
      url="",
      install_requires=['dulwich'],
      packages=find_packages(),
      license='BSD (Simplified)',
      platforms='Posix; MacOS X; Windows',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Topic :: System :: Systems Administration'],
      )
