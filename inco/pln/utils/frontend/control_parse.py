from Tkconstants import END, INSERT
from Tkinter import Text
import tkMessageBox
import ttk

from nltk import Tree

from inco.pln.parse.freeling import FreeLing
from inco.pln.parse.maltparser import MaltParser
from inco.pln.utils.dot_language_converter import DotLanguageConverter
from inco.pln.utils.frontend.configuration_manager import ConfigurationManager


__author__ = 'Matias'


class ControlParse:
    input_text_area = None
    """:type: Tkinter.Text """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)

        ttk.Label(self.frame, text="Input").grid(row=0, column=0, columnspan=2)
        self.input_text_area = Text(self.frame, height=15, width=100)
        self.input_text_area.grid(row=1, column=0, columnspan=2)

        ttk.Button(self.frame, text="Parse with FreeLing", command=self.__parse_with_freeling).grid(row=2, column=0)
        ttk.Button(self.frame, text="Parse with MaltParser", command=self.__parse_with_maltparser).grid(row=2, column=1)

        ttk.Label(self.frame, text="Output").grid(row=3, column=0, columnspan=2)
        self.output_text_area = Text(self.frame, height=15, width=100)
        self.output_text_area.grid(row=4, column=0, columnspan=2)

        ttk.Button(self.frame, text="To DOT Language", command=self.__to_dot).grid(row=5, column=0)
        ttk.Button(self.frame, text="Render tree with NLTK", command=self.__render_tree).grid(row=5, column=1)

        self.output_dot_text_area = Text(self.frame, height=15, width=100)
        self.output_dot_text_area.grid(row=6, column=0, columnspan=2)


    def __parse_with_freeling(self):
        freeling_path = ConfigurationManager.load()['freeling_path']

        if freeling_path is None:
            tkMessageBox.showerror(message='Path to FreeLing not set')
            return

        string = self.input_text_area.get("1.0", END)
        string = string.rstrip()
        string = "[" + string + "]"
        string = string.replace("\n", ",")

        parser = FreeLing(freeling_path)

        tree = parser.parse(string)

        self.output_text_area.delete(1.0, END)

        tree_str = str(tree)

        self.output_text_area.insert(INSERT, str(tree_str))

    def __parse_with_maltparser(self):
        parser_path = ConfigurationManager.load()['maltparser_path']
        parser_model_path = ConfigurationManager.load()['maltparser_model_path']

        if parser_path is None:
            tkMessageBox.showerror(message='Path to MaltParse not set')
            return

        if parser_model_path is None:
            tkMessageBox.showerror(message='Path to MaltParser model not set')
            return

        string = self.input_text_area.get("1.0", END)
        string = string.rstrip()
        string = "[" + string + "]"
        string = string.replace("\n", ",")

        parser = MaltParser(parser_path, parser_model_path)

        tree = parser.parse(string)

        tree_str = str(tree)

        self.output_text_area.delete(1.0, END)
        self.output_text_area.insert(INSERT, tree_str)

    def __to_dot(self):
        string = self.output_text_area.get("1.0", END)
        string = string.replace("\n", "")

        tree = Tree.fromstring(string)

        converter = DotLanguageConverter()
        dotstring = converter.convert(tree)

        self.output_dot_text_area.delete(1.0, END)
        self.output_dot_text_area.insert(INSERT, dotstring)

        pass

    def __render_tree(self):
        string = self.output_text_area.get("1.0", END)
        string = string.replace("\n", "")

        tree = Tree.fromstring(string)

        tree.draw()