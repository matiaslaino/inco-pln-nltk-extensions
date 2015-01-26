# -*- coding: utf-8 -*-
import codecs
import json

from nltk import ParserI

from inco.pln.freeling_base import FreeLingBase
import inco.pln.tagging_constants as constants
from inco.pln.parse.tree.freeling_tree_builder import FreeLingTreeBuilder


__author__ = 'Matias'


class FreeLing(FreeLingBase, ParserI):
    def __init__(self, path_to_tagger, verbose=False):
        self.is_full = False
        self._setup(path_to_tagger, verbose)

    def process_output(self, file_path):
        parse_tree_str = ""

        with codecs.open(file_path, encoding='utf8') as temp_output:
            for line in temp_output:
                parse_tree_str += line
                if self.verbose:
                    print line

        if self.verbose:
            print "Salida de FreeLing: " + parse_tree_str
            print "--- Creando árbol de parseo ---"

        if self.verbose:
            print "--- Construyendo árbol de parseo ---"

        tree_builder = FreeLingTreeBuilder()
        tree = tree_builder.build(parse_tree_str)

        return tree

    def get_type(self):
        return FreeLingBase._type_parser

    def parse(self, sent_str, verbose=False):
        # traducir desde nuestro formato esperado al formato de entrada de FreeLing.
        # nuestro formato es un diccionario.
        # El formato de entrada de FreeLing es:
        # palabra     lemma       pos_tag

        utf8_line = sent_str.decode('utf8')
        line = json.loads(utf8_line)

        str_result = u''

        if verbose:
            print "--- Procesando tokens de entrada  ---"

        try:
            for word_dict in line:
                str_result += u"{} {} {}\n".format(word_dict[constants.WORD], word_dict[constants.LEMMA],
                                                   word_dict[constants.POS_TAG])
        except KeyError, e:
            print e
            exit()

        tree = self.execute(str_result, True)

        return tree