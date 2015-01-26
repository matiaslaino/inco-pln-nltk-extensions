from Tkconstants import END, INSERT
from Tkinter import Text
import tkMessageBox
import ttk

from inco.pln.tokenize.freeling import FreeLing
from inco.pln.utils.frontend.configuration_manager import ConfigurationManager


__author__ = 'Matias'


class ControlTokenize:
    input_text_area = None
    """:type: Tkinter.Text """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)

        ttk.Label(self.frame, text="Input").grid(row=0, column=0, columnspan=2)
        self.input_text_area = Text(self.frame, height=15, width=100)
        self.input_text_area.grid(row=1, column=0, columnspan=2)

        ttk.Button(self.frame, text="Tokenize with FreeLing", command=self.__tokenize_with_freeling).grid(row=2,
                                                                                                          column=0)

        ttk.Label(self.frame, text="Output").grid(row=3, column=0, columnspan=2)
        self.output_text_area = Text(self.frame, height=15, width=100)
        self.output_text_area.grid(row=4, column=0, columnspan=2)
        self.output_text_area['state'] = 'disabled'

    def __tokenize_with_freeling(self):
        freeling_path = ConfigurationManager.load()['freeling_path']

        if freeling_path is None:
            tkMessageBox.showerror(message='Path to FreeLing not set')
            return

        string = self.input_text_area.get("1.0", END)
        tokenizer = FreeLing(freeling_path)

        tokens = tokenizer.tokenize(string)

        tokenized_string = "\n".join(tokens)

        self.output_text_area['state'] = 'normal'

        self.output_text_area.delete(1.0, END)
        self.output_text_area.insert(INSERT, tokenized_string)

        self.output_text_area['state'] = 'disabled'