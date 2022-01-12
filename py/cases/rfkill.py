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
		for filename in scandir('/sys/class/rfkill'):
			if filename.name.startswith('rfkill'):
				with open(PurePath(filename, 'type')) as f:
					rfkill_type = f.read().strip()
				with open(PurePath(filename, 'name')) as f:
					rfkill_name = f.read().strip()
				with open(PurePath(filename, 'hard')) as f:
					rfkill_hard = int(f.read().strip())
				with open(PurePath(filename, 'soft')) as f:
					rfkill_soft = int(f.read().strip())
				yield f'{filename.path} {rfkill_type} {rfkill_name} {rfkill_hard} {rfkill_soft}'

		# 'state' 'device@' 'index' 'persistent' 'power/' 'subsystem@' 'uevent'

	def stop(self):
		pass

