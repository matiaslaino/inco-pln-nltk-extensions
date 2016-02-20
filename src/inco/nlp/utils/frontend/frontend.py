try:
  import Tkinter              # Python 2
  import ttk
  from Tkconstants import BOTH

except ImportError:
  import tkinter as Tkinter   # Python 3
  import tkinter.ttk as ttk
  from tkinter.constants import BOTH


from inco.nlp.utils.frontend.control_parse import ControlParse
from inco.nlp.utils.frontend.control_tag import ControlTag
from inco.nlp.utils.frontend.control_tokenize import ControlTokenize
from inco.nlp.utils.frontend.menu_bar import MenuBar


__author__ = 'Matias Laino'

root = Tkinter.Tk()
root.wm_title('Demo Frontend')

toplevel = root.winfo_toplevel()
toplevel.wm_state('zoomed')

n = ttk.Notebook(root)
MenuBar(root)

n.add(ControlTokenize(n).frame, text='Tokenize')
n.add(ControlTag(n).frame, text='Tag')
n.add(ControlParse(n).frame, text='Parse')
n.pack(expand=True, fill=BOTH)

root.mainloop()