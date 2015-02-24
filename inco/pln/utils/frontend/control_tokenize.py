from Tkconstants import END, INSERT, BOTH
from Tkinter import Text
import Tkinter as tk
import tkMessageBox

from inco.pln.common import UIUtils
from inco.pln.tokenize.freeling import FreeLing
from inco.pln.utils.frontend.configuration_manager import ConfigurationManager


__author__ = 'Matias'


class ControlTokenize:
    input_text_area = None
    """:type: Tkinter.Text """

    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)

        tk.Label(self.frame, text="Input").pack()
        self.input_text_area = Text(self.frame, height=10, width=100)
        self.input_text_area.pack(fill=BOTH, expand=True)
        tk.Button(self.frame, text="Tokenize with FreeLing", command=self.__tokenize_with_freeling).pack()
        tk.Label(self.frame, text="Output").pack()
        self.output_text_area = Text(self.frame, height=10, width=100)
        self.output_text_area.pack(fill=BOTH, expand=True)
        self.output_text_area['state'] = 'disabled'

        # scroll = Scrollbar(self.input_text_area)
        # scroll.config(command=self.input_text_area.yview)
        # self.input_text_area.config(yscrollcommand=scroll.set)
        # scroll.pack(side=RIGHT, fill=Y)

        UIUtils.set_vertical_scroll(self.input_text_area)
        UIUtils.set_vertical_scroll(self.output_text_area)


    def __tokenize_with_freeling(self):
        freeling_path = ConfigurationManager.load()['freeling_path']

        string = self.input_text_area.get("1.0", END)
        tokenizer = FreeLing(freeling_path)

        tokens = tokenizer.tokenize(string)

        tokenized_string = "\n".join(tokens)

        self.output_text_area['state'] = 'normal'

        self.output_text_area.delete(1.0, END)
        self.output_text_area.insert(INSERT, tokenized_string)

        self.output_text_area['state'] = 'disabled'