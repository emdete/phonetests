#!/usr/bin/env python3
__copyright__ = "Copyright (c) 2008-2021 M. Dietrich <mdt@emdete.de>"
__license__ = "GPLv3"

from logging import getLogger
log = getLogger('__name__')
getLogger().addHandler(StreamHandler(open('/var/log/phonetests.log', 'a')))
from os import environ
from os import system

x11 = environ.get('DISPLAY')
wayland = environ.get('WAYLAND_DISPLAY')
term = environ.get('TERM')
if x11 and ':' in x11:
	from x11_display import Display
elif wayland:
	from wayland_display import Display
elif term:
	from curses_display import Display
else:
	from line_display import Display

display = Display()
display.add_display()
display.start()
