import ttk

from inco.pln.utils.frontend.control_parsing import ControlParsing

from inco.pln.utils.frontend.control_tagging import ControlTagging
from inco.pln.utils.frontend.menu_bar import MenuBar


__author__ = 'Matias'

from Tkinter import *

root = Tk()
root.wm_title('Test Frontend')

n = ttk.Notebook(root)

MenuBar(root)

f2 = ttk.Frame(n, width=600, height=600)  # second page
n.add(ControlTagging(n).frame, text='Tagging')
n.add(ControlParsing(n).frame, text='Parsing')
n.pack()

root.mainloop()