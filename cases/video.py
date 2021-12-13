#!/usr/bin/env python3
__copyright__ = 'Copyright (c) 2008-2021 M. Dietrich <mdt@emdete.de>'
__license__ = 'GPLv3'

from os import scandir
import v4l2capture

for filename in scandir('/dev'):
	if filename.name.startswith('video'):
		video = v4l2capture.Video_device(filename.path)
		try:
			driver, card, bus_info, capabilities = video.get_info()
			capabilities = ', '.join([n.decode() for n in capabilities])
			print(f'driver={driver}; card={card}bus; info={bus_info}; capabilities={capabilities}.')
			try:
				print('format', video.get_format())
				for fourcc in video.get_formats():
					for framesize in video.get_framesizes(fourcc):
						x, y = framesize['size_x'], framesize['size_y']
						for frameinterval in video.get_frameintervals(fourcc, x, y):
							print('\t', fourcc.decode(), x, y, frameinterval['fps'])
			except:
				pass
		finally:
			video.close()

