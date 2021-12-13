#!/usr/bin/env python3
__copyright__ = 'Copyright (c) 2008-2021 M. Dietrich <mdt@emdete.de>'
__license__ = 'GPLv2'

from os import scandir
from pathlib import PurePath

from logging import getLogger
logger = getLogger(__name__)

class Case(object):
	def __init__(self, stdscr):
		pass

	def start(self):
		return
		_PATH_DEV_RFKILL = '/dev/rfkill'

		for filename in scandir('/sys/devices/virtual/thermal'):
			if filename.name.startswith('thermal_zone'):
				with open(PurePath(filename, 'type')) as f:
					thermal_type = f.read().strip()
				with open(PurePath(filename, 'temp')) as f:
					thermal_temp = int(f.read().strip()) / 1000
				print(f'{filename.path} {thermal_type} {thermal_temp}')

	def stop(self):
		pass


