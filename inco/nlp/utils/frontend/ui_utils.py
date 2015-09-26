from Tkconstants import RIGHT, END, INSERT
from Tkconstants import Y
import Tkinter as tk
import codecs
import threading
import tkFileDialog

__author__ = 'Matias Laino'


class UIUtils:
    @staticmethod
    def set_vertical_scroll(widget):
        """
        @param widget:
        @type widget: tk.Widget
        """

        scroll = tk.Scrollbar(widget)
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
