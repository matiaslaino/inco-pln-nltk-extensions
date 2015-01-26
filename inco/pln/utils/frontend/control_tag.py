from Tkconstants import END, INSERT
from Tkinter import Text
import json
import tkMessageBox
import ttk

from inco.pln.tag.freeling import FreeLing
from inco.pln.tag.treetagger import TreeTagger
from inco.pln.utils.frontend.configuration_manager import ConfigurationManager


__author__ = 'Matias'


class ControlTag:
    input_text_area = None
    """:type: Tkinter.Text """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)

        ttk.Label(self.frame, text="Input").grid(row=0, column=0, columnspan=2)
        self.input_text_area = Text(self.frame, height=15, width=100)
        self.input_text_area.grid(row=1, column=0, columnspan=2)

        ttk.Button(self.frame, text="Tag with FreeLing", command=self.__tag_with_freeling).grid(row=2, column=0)
        ttk.Button(self.frame, text="Tag with TreeTagger", command=self.__tag_with_treetagger).grid(row=2, column=1)

        ttk.Label(self.frame, text="Output").grid(row=3, column=0, columnspan=2)
        self.output_text_area = Text(self.frame, height=15, width=100)
        self.output_text_area.grid(row=4, column=0, columnspan=2)
        self.output_text_area['state'] = 'disabled'


    def __tag_with_freeling(self):
        freeling_path = ConfigurationManager.load()['freeling_path']

        if freeling_path is None:
            tkMessageBox.showerror(message='Path to FreeLing not set')
            return

        string = self.input_text_area.get("1.0", END)
        tokenizer = FreeLing(freeling_path)

        tokens_dict = tokenizer.tag_string_full(string)

        tokens_dict_array = [json.dumps(x) for x in tokens_dict]

        tokenized_string = "\n".join(tokens_dict_array)

        self.output_text_area['state'] = 'normal'

        self.output_text_area.delete(1.0, END)
        self.output_text_area.insert(INSERT, tokenized_string)

        self.output_text_area['state'] = 'disabled'

    def __tag_with_treetagger(self):
        path = ConfigurationManager.load()['treetagger_path']

        if path is None:
            tkMessageBox.showerror(message='Path to TreeTagger not set')
            return

        string = self.input_text_area.get("1.0", END)
        tokenizer = TreeTagger(path)

        tokens_dict = tokenizer.tag_string_full(string)

        tokens_dict_array = [str(x) for x in tokens_dict]

        tokenized_string = "\n".join(tokens_dict_array)

        self.output_text_area['state'] = 'normal'

        self.output_text_area.delete(1.0, END)
        self.output_text_area.insert(INSERT, tokenized_string)

        self.output_text_area['state'] = 'disabled'