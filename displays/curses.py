from logging import getLogger
log = getLogger('__name__')
from curses import wrapper

class Display(object):
	def __init__(self):
		pass

	def start(self):
		wrapper(self.main)

	def main(self, stdscr):
		self.stdscr = stdscr
		self.stdscr.clear()

	def _():
		self.stdscr.addstr(0, 0, '')
		self.stdscr.refresh()
		self.stdscr.addstr(1, 0, f'Pos {p}')
		self.stdscr.addstr(0, 0, f'Time {p}')
		self.stdscr.addstr(i+1, 0, f'{source}-{i}: {s}')

