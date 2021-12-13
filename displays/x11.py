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
		self.ti = self.canvas.create_text((200, 100), fill='gray', )

	def add_display(self):
		self.canvas.itemconfig(self.ti, text='Sat: {}/{}/{}'.format(0, 0, 0), font=('Sans', 100, 'bold', ))

	def stop(self, event):
		self.tk.quit()

	def start(self):
		mainloop()

	def _configure(self, event):
		if self.width != event.width and self.height != event.height:
			self.width, self.height = event.width, event.height
			self.canvas.config(width=self.width, height=self.height, )
			self.canvas.pack()
			self.canvas.coords(self.ti, self.width//2, self.height//2)

