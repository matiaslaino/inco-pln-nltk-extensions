from threading import Thread
from inco.nlp.utils.frontend.progress_dialog import ProgressDialog

try:
  import Tkinter              # Python 2
  import ttk
  from Tkconstants import END, INSERT, W, E, S, N, HORIZONTAL
except ImportError:
  import tkinter as Tkinter   # Python 3
  import tkinter.ttk as ttk
  from tkinter.constants import END, INSERT, W, E, S, N, HORIZONTAL


from nltk import Tree

from inco.nlp.tag.treetagger import TreeTagger
from inco.nlp.utils.frontend.ui_utils import UIUtils
import inco.nlp.tag.freeling
from inco.nlp.parse.stanford.stanford_shift_reduce import StanfordShiftReduceParser
from inco.nlp.parse.freeling import FreeLing
from inco.nlp.parse.maltparser import MaltParser
from inco.nlp.utils.dot_language_converter import DotLanguageConverter
from inco.nlp.utils.frontend.configuration_manager import ConfigurationManager

__author__ = 'Matias Laino'


class ControlParse:
    input_text_area = None
    """@type: Tkinter.Text """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)

        columns = 5

        ttk.Label(self.frame, text="Input").grid(row=0, column=0, columnspan=columns)
        self.input_text_area = Tkinter.Text(self.frame, width=100)
        self.input_text_area.grid(row=1, column=0, columnspan=columns, sticky=N + S + E + W)
        ttk.Button(self.frame, text="Read from file", command=self.__read_from_file) \
            .grid(row=0, column=2, columnspan=2)

        ttk.Button(self.frame, text="Parse with FreeLing", command=self.__on_parse_with_freeling_click).grid(row=2, column=1,
                                                                                                    sticky=N + S + E + W)
        ttk.Button(self.frame, text="Parse with MaltParser", command=self.__on_parse_with_maltparser_click).grid(row=2, column=2,
                                                                                                        sticky=N + S + E + W)
        ttk.Button(self.frame, text="Parse with Stanford SR", command=self.__on_parse_with_stanford_click).grid(row=2, column=3,
                                                                                                       sticky=N + S + E + W)

        self.tagger_var = Tkinter.StringVar()
        self.tagger_box = ttk.Combobox(self.frame, textvariable=self.tagger_var);
        self.tagger_box['values'] = ('FreeLing', 'TreeTagger')
        self.tagger_box.current(0)
        self.tagger_box.grid(row=2, column=0)
        self.tagger_box.state(['readonly'])

        ttk.Label(self.frame, text="Output").grid(row=3, column=0, columnspan=columns)
        self.output_text_area = Tkinter.Text(self.frame, width=100)
        self.output_text_area.grid(row=4, column=0, columnspan=columns, sticky=N + S + E + W)

        ttk.Button(self.frame, text="To DOT Language", command=self.__to_dot).grid(row=5, column=1,
                                                                                   sticky=N + S + E + W)
        ttk.Button(self.frame, text="Render tree with NLTK", command=self.__render_tree).grid(row=5, column=3,
                                                                                              sticky=N + S + E + W)

        self.output_dot_text_area = Tkinter.Text(self.frame, width=100)
        self.output_dot_text_area.grid(row=6, column=0, columnspan=columns, sticky=N + S + E + W)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_columnconfigure(4, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)
        self.frame.grid_rowconfigure(6, weight=1)

        UIUtils.set_vertical_scroll(self.input_text_area)
        UIUtils.set_vertical_scroll(self.output_text_area)
        UIUtils.set_vertical_scroll(self.output_dot_text_area)

    def __parse_with_freeling(self):
        self.progressDialog = ProgressDialog(self.parent)

        try:

            freeling_path = ConfigurationManager.load()['freeling_path']

            string = self.input_text_area.get("1.0", END)

            if self.tagger_var.get() == 'FreeLing':
                tagger = None
            else:
                tagger_path = ConfigurationManager.load()['treetagger_path']
                tagger = TreeTagger(tagger_path)

            parser = FreeLing(freeling_path, tagger=tagger)

            tree = next(parser.raw_parse(string))

            self.output_text_area.delete(1.0, END)

            tree_str = str(tree)

            self.output_text_area.insert(INSERT, str(tree_str))
        finally:
            self.stop_progressbar()

    def __on_parse_with_freeling_click(self):
        parse_thread = Thread(target=self.__parse_with_freeling)
        parse_thread.start()

    def __on_parse_with_maltparser_click(self):
        parse_thread = Thread(target=self.__parse_with_maltparser)
        parse_thread.start()

    def __on_parse_with_stanford_click(self):
        parse_thread = Thread(target=self.__parse_with_stanford)
        parse_thread.start()

    def __parse_with_maltparser(self):
        self.progressDialog = ProgressDialog(self.parent)

        try:
            parser_path = ConfigurationManager.load()['maltparser_path']
            parser_model_path = ConfigurationManager.load()['maltparser_model_path']

            if self.tagger_var.get() == 'FreeLing':
                tagger_path = ConfigurationManager.load()['freeling_path']
                tagger = inco.nlp.tag.freeling.FreeLing(tagger_path)
            else:
                tagger_path = ConfigurationManager.load()['treetagger_path']
                tagger = TreeTagger(tagger_path)

            string = self.input_text_area.get("1.0", END)

            parser = MaltParser(parser_path, parser_model_path, tagger=tagger)

            tree = next(parser.raw_parse(string))

            tree_str = str(tree)

            self.output_text_area.delete(1.0, END)
            self.output_text_area.insert(INSERT, tree_str)
        finally:
            self.stop_progressbar()

    def __parse_with_stanford(self):
        self.progressDialog = ProgressDialog(self.parent)

        try:
            parser_path = ConfigurationManager.load()['stanfordsr_path']
            parser_model_path = ConfigurationManager.load()['stanfordsr_model_path']
            freeling_path = ConfigurationManager.load()['freeling_path']

            string = self.input_text_area.get("1.0", END)
            # string = string.rstrip()
            # string = "[" + string + "]"
            # string = string.replace("\n", ",")

            tagger = inco.nlp.tag.freeling.FreeLing(freeling_path)

            parser = StanfordShiftReduceParser(parser_path, parser_model_path, tagger=tagger)

            tree = next(parser.raw_parse(string))

            tree_str = str(tree)

            self.output_text_area.delete(1.0, END)
            self.output_text_area.insert(INSERT, tree_str)
        finally:
            self.stop_progressbar()

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
        # self.progressDialog = ProgressDialog(self.parent)
        # self.parent.after(2000, self.stop_progressbar)


    def stop_progressbar(self):
        self.progressDialog.close()

    def __read_from_file(self):
        UIUtils.read_from_file_to_input(self.input_text_area)


