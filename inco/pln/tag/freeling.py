# coding=utf-8
import re

from inco.pln.freeling_base import FreeLingBase


__author__ = 'Matias'

from nltk import TaggerI
import inco.pln.tagging_constants as constants


class FreeLing(TaggerI, FreeLingBase):
    """
    FreeLing tagger wrapper
    """

    def __init__(self, path_to_tagger, verbose=False):
        """
        Constructor.

        :param path_to_tagger: path to binary
        :type path_to_tagger: str
        :param verbose: indicates if additional information should be outputted
        :type verbose: bool
        """
        self.is_full = False
        self._initialize(path_to_tagger, verbose)

    def process_output(self, file_path):
        """
        Processes the complete output of FreeLing when configured as a tagger.

        :param file_path: path to the output to process.
        :type file_path: str
        :return: the list of tagged tokens, each one as a dictionary containing information on the token.
        :rtype: list(dict)
        """

        result = []

        with open(file_path) as output_file:
            for line in output_file:
                if self.verbose:
                    print "Raw FreeLing output: " + line

                if line != "\n":
                    converted_line = FreeLing.__convert_line(line)

                    # todo: add each dictionary directly...
                    if self.is_full:
                        # in full mode is where the most information on a token is provided
                        result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                            (constants.LEMMA, converted_line[constants.LEMMA]),
                                            (constants.COARSE_TAG, converted_line[constants.COARSE_TAG]),
                                            (constants.POS_TAG, converted_line[constants.POS_TAG]),
                                            (constants.FEATURES, dict([
                                                (constants.TAGGER, constants.TAGGERS_FREELING),
                                                (constants.PROBABILITY, converted_line[constants.PROBABILITY])
                                            ]))]))
                    else:
                        # in standard mode, only the word and tags are provided for each token.
                        result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                            (constants.ORIGINAL_TAG, converted_line[constants.ORIGINAL_TAG])]))

        return result

    def get_type(self):
        return FreeLingBase._type_tagger

    def tag(self, tokens):
        """
        Tags a collection of tokens.

        :param tokens: the collection of tokens to POS tag.
        :type tokens: list(str)
        :return: the collection of tokens, POS tagged. Each entry contains: WORD POS-TAG
        :rtype: list(dict)
        """
        string = "\n".join(tokens)
        return self.execute(string, True)

    def tag_full(self, tokens):
        """
        Tags a collection of tokens.

        :param tokens: the collection of tokens to POS tag.
        :type tokens: list(str)
        :return: the collection of tokens, POS tagged. Each entry contains: WORD LEMMA COARSE-TAG POS-TAG FEATURES
        :rtype: list(dict)
        """

        self.is_full = True
        string = "\n".join(tokens)
        return self.execute(string, True)

    def tag_string_full(self, string):
        """
        Tags a collection of tokens.

        :param string: string to POS tag.
        :type string: str
        :return: the collection of tokens, POS tagged. Each entry contains: WORD LEMMA COARSE-TAG POS-TAG FEATURES
        :rtype: list(dict)
        """

        self.is_full = True

        return self.execute(string, False)

    @staticmethod
    def __convert_line(input_line):
        """
        Converts a single line of FreeLing output into a dictionary.

        dictionary keys:
            word
            lemma
            original_tag
            coarse_tag
            pos_tag
            probability

        :param input_line: line to convert from FreeLing format to a dictionary.
        :type input_line: str
        :return the FreeLing output line, formatted into a dictionary
        :rtype: dict

        """
        # regular expression to recognize: word lemma coarse-tag pos-tag original-tag
        tree_tagger_regular_expression = re.compile("^(.*)? (.*)? (.*)? (.*)?")

        utf8line = input_line.decode('utf-8')
        parsed_line = tree_tagger_regular_expression.match(utf8line)

        result_object = {constants.WORD: parsed_line.group(1), constants.LEMMA: parsed_line.group(2),
                         constants.ORIGINAL_TAG: parsed_line.group(3),
                         constants.COARSE_TAG: parsed_line.group(3)[0], constants.POS_TAG: parsed_line.group(3),
                         constants.PROBABILITY: parsed_line.group(4)}

        return result_object
