# coding=utf-8
import re

from inco.pln.freeling_base import FreeLingBase


__author__ = 'Matias'

from nltk import TaggerI
import inco.pln.tagging_constants as constants


class FreeLing(TaggerI, FreeLingBase):
    def __init__(self, path_to_tagger, verbose=False):
        self.is_full = False
        self._setup(path_to_tagger, verbose)
        # self._process_output = self.__process_output

    def process_output(self, file_path):
        result = []

        # hay que procesar el archivo leido, hay que leerlo primero.
        with open(file_path) as output_file:
            for line in output_file:
                if self.verbose:
                    print "Salida de FreeLing: " + line

                if line != "\n":
                    converted_line = FreeLing.__convert_line(line)

                    if self.is_full:
                        result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                            (constants.LEMMA, converted_line[constants.LEMMA]),
                                            (constants.COARSE_TAG, converted_line[constants.COARSE_TAG]),
                                            (constants.POS_TAG, converted_line[constants.POS_TAG]),
                                            (constants.FEATURES, dict([
                                                (constants.TAGGER, constants.TAGGERS_FREELING),
                                                (constants.PROBABILITY, converted_line[constants.PROBABILITY])
                                            ]))]))
                    else:
                        result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                            (constants.ORIGINAL_TAG, converted_line[constants.ORIGINAL_TAG])]))

        return result

    def get_type(self):
        return FreeLingBase._type_tagger

    def tag(self, tokens):
        string = "\n".join(tokens)
        return self._execute(string, True)

    def tag_full(self, tokens):
        self.is_full = True
        string = "\n".join(tokens)
        return self._execute(string, True)

    def tag_string_full(self, string):
        self.is_full = True

        return FreeLing._execute(string, False)

    @staticmethod
    def __convert_line(input_line):
        """
        Convierte una linea de output de TreeTagger a un diccionario.

        claves del diccionario:
            word
            lemma
            original_tag
            coarse_tag
            pos_tag
            probability
        """
        # forma: palabra, lemma, coarse tag, pos tag, original tag
        tree_tagger_regular_expression = re.compile("^(.*)? (.*)? (.*)? (.*)?")

        utf8line = input_line.decode('utf-8')
        parsed_line = tree_tagger_regular_expression.match(utf8line)
        # print utf8line
        result_object = {constants.WORD: parsed_line.group(1), constants.LEMMA: parsed_line.group(2),
                         constants.ORIGINAL_TAG: parsed_line.group(3),
                         constants.COARSE_TAG: parsed_line.group(3)[0], constants.POS_TAG: parsed_line.group(3),
                         constants.PROBABILITY: parsed_line.group(4)}

        return result_object
