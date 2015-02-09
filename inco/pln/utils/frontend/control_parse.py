from Tkconstants import END, INSERT, W, E, S, N
from Tkinter import Text
import tkMessageBox
import ttk

from nltk import Tree
from inco.pln.common import UIUtils

import inco.pln.tag.freeling
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

        columns = 4

        ttk.Label(self.frame, text="Input").grid(row=0, column=0, columnspan=columns)
        self.input_text_area = Text(self.frame, width=100)
        self.input_text_area.grid(row=1, column=0, columnspan=columns, sticky=N+S+E+W)

        ttk.Button(self.frame, text="Parse with FreeLing", command=self.__parse_with_freeling).grid(row=2, column=1, sticky=N+S+E+W)
        ttk.Button(self.frame, text="Parse with MaltParser", command=self.__parse_with_maltparser).grid(row=2, column=2, sticky=N+S+E+W)

        ttk.Label(self.frame, text="Output").grid(row=3, column=0, columnspan=columns)
        self.output_text_area = Text(self.frame, width=100)
        self.output_text_area.grid(row=4, column=0, columnspan=columns, sticky=N+S+E+W)

        ttk.Button(self.frame, text="To DOT Language", command=self.__to_dot).grid(row=5, column=1, sticky=N+S+E+W)
        ttk.Button(self.frame, text="Render tree with NLTK", command=self.__render_tree).grid(row=5, column=2, sticky=N+S+E+W)

        self.output_dot_text_area = Text(self.frame, width=100)
        self.output_dot_text_area.grid(row=6, column=0, columnspan=columns, sticky=N+S+E+W)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(6, weight=1)

        UIUtils.set_vertical_scroll(self.input_text_area)
        UIUtils.set_vertical_scroll(self.output_text_area)
        UIUtils.set_vertical_scroll(self.output_dot_text_area)

    def __parse_with_freeling(self):
        freeling_path = ConfigurationManager.load()['freeling_path']

        if freeling_path is None:
            tkMessageBox.showerror(message='Path to FreeLing not set')
            return

        string = self.input_text_area.get("1.0", END)
        # string = string.rstrip()
        # string = "[" + string + "]"
        # string = string.replace("\n", ",")

        parser = FreeLing(freeling_path)

        tree = parser.raw_parse(string)[0]

        self.output_text_area.delete(1.0, END)

        tree_str = str(tree)

        self.output_text_area.insert(INSERT, str(tree_str))

    def __parse_with_maltparser(self):
        parser_path = ConfigurationManager.load()['maltparser_path']
        parser_model_path = ConfigurationManager.load()['maltparser_model_path']
        freeling_path = ConfigurationManager.load()['freeling_path']

        if parser_path is None:
            tkMessageBox.showerror(message='Path to MaltParse not set')
            return

        if parser_model_path is None:
            tkMessageBox.showerror(message='Path to MaltParser model not set')
            return

        if freeling_path is None:
            tkMessageBox.showerror(message='Path to FreeLing not set')
            return

        string = self.input_text_area.get("1.0", END)
        # string = string.rstrip()
        # string = "[" + string + "]"
        # string = string.replace("\n", ",")

        tagger = inco.pln.tag.freeling.FreeLing(freeling_path)

        parser = MaltParser(parser_path, parser_model_path, tagger=tagger)

        tree = parser.raw_parse(string)[0]

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