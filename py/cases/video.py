#!/usr/bin/env python3
__copyright__ = 'Copyright (c) 2008-2021 M. Dietrich <mdt@emdete.de>'
__license__ = 'GPLv2'

from os import scandir
import v4l2capture
from contextlib import closing

from logging import getLogger
logger = getLogger(__name__)

class Case(object):
	def __init__(self, stdscr):
		pass

	def start(self):
		for filename in scandir('/dev'):
			if filename.name.startswith('video'):
				with closing(v4l2capture.Video_device(filename.path) as video:
					driver, card, bus_info, capabilities = video.get_info()
					capabilities = ', '.join([n.decode() for n in capabilities])
					yield f'{filename.name}; driver={driver}; card={card}bus; info={bus_info}; capabilities={capabilities}'
					try:
						yield '\tformat {}'.format(video.get_format())
						for fourcc in video.get_formats():
							for framesize in video.get_framesizes(fourcc):
								x, y = framesize['size_x'], framesize['size_y']
								for frameinterval in video.get_frameintervals(fourcc, x, y):
									yield '\t\t{} {} {} {}'.format(fourcc.decode(), x, y, frameinterval['fps'])
					except:
						yield 'error'

	def stop(self):
		pass

