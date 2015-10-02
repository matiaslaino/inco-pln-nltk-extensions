# -*- coding: utf-8 -*-
import codecs

from nltk.tokenize.api import TokenizerI

from inco.nlp.freeling_base import FreeLingBase

__author__ = 'Matias Laino'


class FreeLing(FreeLingBase, TokenizerI):
    """
    Wrapper class for the FreeLing tokenizer.
    """

    def __init__(self, path_to_tagger, verbose=False):
        """
        Constructor.

        @param path_to_tagger: path to binary
        @type path_to_tagger: str
        @param verbose: indicates if additional information should be outputted
        @type verbose: bool
        """
        self._initialize(path_to_tagger, verbose)

    def tokenize(self, string):
        """
        Tokenizes an input string.

        @param string: input string to be tokenized.
        @type string: unicode
        @return: the input string, tokenized.
        @rtype: list(str)
        """

        # hack: add two newlines to prevent FreeLing from repeating output...
        string += "\n\n"
        return self.execute(string, self._format_type_plain, self._format_type_tokenized)

    def process_output(self, file_path):
        """
        Processes the complete output of FreeLing when configured as a tokenizer.

        @param file_path: path to the output to process.
        @type file_path: str
        @return: the list of tokens.
        @rtype: list(str)
        """

        result = []

        # process output file.
        # todo: move this code to base class?
        with codecs.open(file_path, encoding='utf8') as temp_output:
            for line in temp_output:

                result.append(line.rstrip())
                if self.verbose:
                    print(line)

        return result