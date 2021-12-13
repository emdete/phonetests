# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas-methods.html
from logging import getLogger
log = getLogger('__name__')
from tkinter import Tk, Canvas, mainloop

class Display(object):
	def __init__(self):
		self.width, self.height = 0, 0
		self.tk = Tk()
		self.tk.attributes('-fullscreen', True)
		for n in ('<Control-q>', '<Control-w>', '<Control-x>', '<Alt-F4>', 'q', ):
			self.tk.bind_all(n, self.stop)
		self.tk.bind('<Configure>', self._configure)
		self.canvas = Canvas(self.tk, cursor='none', borderwidth=0, background='black', highlightthickness=0, )
		#self.canvas.after(randint(l * 3000, l * 5000), tchange)
		self.cases = dict()
		self.tis = dict()
		self.tk.bind_all('<<Data>>', self._data)

	def send_data(self, name, **argv):
		self.tk.event_generate('<<Data>>', name=name, **argv)

	def _data(self, name, **argv):
		self.canvas.itemconfig(self.tis[name], text='{}'.format(name), font=('Iosevka', 20, 'normal', ))

	def start(self):
		for case in self.cases.values():
			case.start()
		mainloop()

	def stop(self, event):
		for case in self.cases.values():
			case.stop()
		self.tk.quit()

	def add_display(self, name, module):
		self.cases[name] = module.Case(self)
		self.tis[name] = self.canvas.create_text((200, 100), fill='gray', )
		self.canvas.itemconfig(self.tis[name], text='{}'.format(name), font=('Iosevka', 20, 'normal', ))

	def _configure(self, event):
		if self.width != event.width and self.height != event.height:
			self.width, self.height = event.width, event.height
			self.canvas.config(width=self.width, height=self.height, )
			self.canvas.pack()
			self._order()

	def _order(self):
			y = 40
			for name in sorted(self.tis.keys()):
				self.canvas.coords(self.tis[name], self.width//2, y)
				y += 40

