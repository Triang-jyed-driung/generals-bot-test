from tkinter import *
from tkinter import ttk
from threading import Thread
import threading

class GUI:
	def __init__(self,info):
		def mainthread(info):
			root = Tk()
			rows = info['rows']
			cols = info['cols']
			turn = info['turn'] / 2
			bingzhong=info['tile_grid']
			bingli=info['army_grid']
			ta=info['cities']
			wang=info['generals']
			colorlist=['#FF0000','#4363D8','#008000','#00C080',
				'#F58231','#F032E6','#800080','#800000','#202020','#808080','#202020','#808080']

			self.table = [([0]*cols) for _ in range(rows)]

			for i in range(rows):
				for j in range(cols):
					
					color=colorlist[bingzhong[i][j]]
					text=''
					# if (i,j) in ta: text+='T'
					if (i,j) in wang: text+='G'
					if bingzhong[i][j] in[-2,-4]: text+='M'
					if bingli[i][j] != 0: text+=str(bingli[i][j])

					self.table[i][j]=ttk.Label(root,
						text=text, background=color, foreground='#FFFFFF',
						font=('Consolas',17))
					self.table[i][j].grid(row=i,column=j)

			root.mainloop()
		tmain=threading.Thread(target=mainthread, args=(info,))
		tmain.start()
	def updateinfo(self,info):
		rows = info['rows']
		cols = info['cols']
		turn = info['turn'] / 2
		bingzhong=info['tile_grid']
		bingli=info['army_grid']
		ta=info['cities']
		wang=info['generals']
		colorlist=['#FF0000','#4363D8','#008000','#00C080',
			'#F58231','#F032E6','#800080','#800000','#808080','#A0A0A0','#808080','#A0A0A0']

		for i in range(rows):
			for j in range(cols):
				color=colorlist[bingzhong[i][j]]
				text=''
				if (i,j) in ta: text+='T'
				else:
					if bingzhong[i][j] in [-3,-1]: color='#909090'
				if (i,j) in wang: text+='G'
				if bingzhong[i][j] in[-2,-4]: text+='-'
				if bingli[i][j] != 0: text+=str(bingli[i][j])
				if (len(text)<3): text += ' ' * (3-len(text))
				self.table[i][j].configure(text=text, background=color)
