try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import gitsecrets

long_description = open('README.md').read()

setup(name="python-git-secrets",
      version=gitsecrets.__version__,
      description="Python implementation of git-secrets",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/mbacchi/python-git-secrets",
      author='Matt Bacchi',
      author_email='mbacchi@gmail.com',
      install_requires=['dulwich'],
      packages=find_packages(),
      license='BSD (Simplified)',
      platforms='Posix; MacOS X; Windows',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Topic :: System :: Systems Administration'],
      python_requires='>=3',
      )
