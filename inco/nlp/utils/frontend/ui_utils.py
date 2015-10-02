import codecs
import threading

try:
    import Tkinter              # Python 2
    import ttk
    import tkFileDialog
    from Tkconstants import RIGHT, END, INSERT, Y, W, E, S, N
except ImportError:
    import tkinter as Tkinter   # Python 3
    import tkinter.ttk as ttk
    from tkinter.constants import RIGHT, END, INSERT, Y,  W, E, S, N
    import tkinter.filedialog as tkFileDialog

__author__ = 'Matias Laino'


class UIUtils:
    @staticmethod
    def set_vertical_scroll(widget):
        """
        @param widget:
        @type widget: tk.Widget
        """

        scroll = Tkinter.Scrollbar(widget)
        scroll.config(command=widget.yview)
        widget.config(yscrollcommand=scroll.set)

        scroll.pack(side=RIGHT, fill=Y)

    @staticmethod
    def read_from_file_to_input(tk_text):
        """
        @type tk_text: Tkinter.Text
        """

        filename = tkFileDialog.askopenfilename()
        string = u""
        with codecs.open(filename, encoding='utf-8') as open_file:
            for line in open_file:
                string = string + line

        tk_text.delete(1.0, END)
        tk_text.insert(INSERT, string)
