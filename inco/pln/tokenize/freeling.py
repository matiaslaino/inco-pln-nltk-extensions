# -*- coding: utf-8 -*-
import codecs

from nltk.tokenize.api import TokenizerI

from inco.pln.freeling_base import FreeLingBase

__author__ = 'Matias'


class FreeLing(FreeLingBase, TokenizerI):
    def __init__(self, path_to_tagger, verbose=False):
        self._setup(path_to_tagger, verbose)

    def tokenize(self, string):
        # hack: add two newlines to prevent FreeLing from repeating output...
        string += "\n\n"
        return self._execute(string, False)

    def process_output(self, file_path):
        result = []

        # hay que procesar el archivo leido, hay que leerlo primero.
        with codecs.open(file_path, encoding='utf8') as temp_output:
            for line in temp_output:

                result.append(line.rstrip())
                if self.verbose:
                    print line

        return result

    def get_type(self):
        return FreeLingBase._type_tokenizer