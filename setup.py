#!/usr/bin/env python
#
# phonetests setup script
# Setup.py for phonetests
#
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
	name = "phonetests",
	version = "0.0.0",
	description = "various phone tests",
	long_description='''
Several tests to show the supported hardware in a linux driven mobile device.
''',
	author = "M. Dietrich",
	author_email = "mdt@emdete.de",
	url = "https://codeberg.org/Belphegor/phonetests",
	packages=[ 'cases', 'displays', ],
	data_files=(('bin/', ('bin/phonetests', ), ), ),
	)

