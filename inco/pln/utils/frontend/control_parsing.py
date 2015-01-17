from Tkinter import Text
import tkMessageBox
import ttk

from inco.pln.tag.freeling import FreeLing
from inco.pln.tag.treetagger import TreeTagger
from inco.pln.utils.frontend.configuration_manager import ConfigurationManager


__author__ = 'Matias'


class ControlParsing:
    input_text_area = None
    """:type: Tkinter.Text """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, width=600, height=600)

        ttk.Label(self.frame, text="Input").grid(row=0, column=0, columnspan=2)
        input_text_area = Text(self.frame, height=15, width=100)
        input_text_area.grid(row=1, column=0, columnspan=2)

        ttk.Button(self.frame, text="Tag with FreeLing", command=self.__tag_with_freeling).grid(row=2, column=0)
        ttk.Button(self.frame, text="Tag with TreeTagger", command=self.__tag_with_treetagger).grid(row=2, column=1)

        ttk.Label(self.frame, text="Output").grid(row=3, column=0, columnspan=2)
        output_text_area = Text(self.frame, height=15, width=100)
        output_text_area.grid(row=4, column=0, columnspan=2)
        output_text_area['state'] = 'disabled'


    def __tag_with_freeling(self):
        if ConfigurationManager.freeling_path is None:
            tkMessageBox.showerror(message='Path to FreeLing not set')
            return

        FreeLing(ConfigurationManager.freeling_path).tag_string_full(self.input_text_area.get(0))

    def __tag_with_treetagger(self):
        if ConfigurationManager.freeling_path is None:
            tkMessageBox.showerror(message='Path to FreeLing not set')
            return

        TreeTagger(ConfigurationManager.treetagger_path).tag_string_full(self.input_text_area.get(0))