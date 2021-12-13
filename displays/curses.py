
from curses import wrapper
				self.stdscr.addstr(0, 0, '')
				self.stdscr.refresh()
		self.stdscr.addstr(1, 0, f'Pos {p}')
		self.stdscr.addstr(0, 0, f'Time {p}')
					self.stdscr.addstr(i+1, 0, f'{source}-{i}: {s}')
	stdscr.clear()
if __name__ == '__main__':
	wrapper(main)
