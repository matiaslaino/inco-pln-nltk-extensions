# -*- coding: utf-8 -*-
import codecs
import json

from nltk import ParserI

from inco.pln.freeling_base import FreeLingBase
import inco.pln.tagging_constants as constants
from inco.pln.parse.tree.freeling_tree_builder import FreeLingTreeBuilder


__author__ = 'Matias'


class FreeLing(FreeLingBase, ParserI):
    """
    FreeLing parser wrapper.
    """

    def __init__(self, path_to_tagger, verbose=False):
        """
        Constructor.
        :param path_to_tagger: path to the FreeLing executable.
        :type path_to_tagger: str
        :param verbose: indicates if additional information will be outputted to the standard output.
        :type verbose: bool
        """
        self.is_full = False
        self._initialize(path_to_tagger, verbose)

    def process_output(self, file_path):
        """
        Processes the complete output of FreeLing when configured as a parser.

        :param file_path: path to the output to process.
        :return: the processed parse tree.
        :rtype: nltk.tree.Tree
        """

        parse_tree_str = ""

        with codecs.open(file_path, encoding='utf8') as temp_output:
            for line in temp_output:
                parse_tree_str += line
                if self.verbose:
                    print line

        if self.verbose:
            print "FreeLing raw output: " + parse_tree_str
            print "--- Building parse tree ---"

        tree_builder = FreeLingTreeBuilder()
        tree = tree_builder.build(parse_tree_str)

        return tree

    def get_type(self):
        return FreeLingBase._type_parser

    def parse(self, input_str, verbose=False):
        """
        Entry point for the FreeLing parser.
        Converts the input string, from our own format, to the expected format of FreeLing.

        :param input_str: input string
        :type input_str: str
        :param verbose: indicate if additional output will be sent to standard output.
        :return: the processed parse tree.
        :rtype: nltk.tree.Tree
        """

        # the expected FreeLing format is:
        # word TAB lemma TAB pos_tag
        # our internal format is a dictionary saved as json.

        utf8_line = input_str.decode('utf8')
        line = json.loads(utf8_line)

        str_result = u''

        if verbose:
            print "--- Processing input ---"

        try:
            for word_dict in line:
                if verbose:
                    print "raw line: " + line

                str_result += u"{} {} {}\n".format(word_dict[constants.WORD], word_dict[constants.LEMMA],
                                                   word_dict[constants.POS_TAG])
        except KeyError, e:
            print e
            exit()

        if verbose:
            print "result: " + str_result

        tree = self.execute(str_result, True)

        return tree

    def grammar(self):
        raise NotImplementedError()