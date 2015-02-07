# -*- coding: utf-8 -*-
import codecs

from nltk import ParserI

from inco.pln.freeling_base import FreeLingBase
from inco.pln.parse.tree.freeling_tree_builder import FreeLingTreeBuilder


__author__ = 'Matias'


class FreeLing(FreeLingBase, ParserI):
    """
    FreeLing parser wrapper.

    EAGLES tagset
    """

    def __init__(self, path_to_tagger=None, verbose=False):
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

    def parse(self, sent):
        """
        :param sent:
        :type sent: list(str)
        :rtype: iter(Tree)
        """

        formatted_str = "\n".join(sent)

        tree = self.execute(formatted_str, self._format_type_tokenized, self._format_type_parsed)

        return [tree]

    def raw_parse(self, sent):
        """
        :param sent:
        :type sent: str
        :rtype: iter(Tree)
        """

        tree = self.execute(sent, self._format_type_plain, self._format_type_parsed)

        return [tree]

    def tagged_parse(self, sent, verbose=False):
        """

        :param sent: input sentence
        :type sent: list(tuple(str, str))
        :return: the processed parse tree.
        :rtype: nltk.tree.Tree
        """

        # the expected FreeLing format is:
        # word TAB lemma TAB pos_tag

        formatted_str_list = map(lambda item: u"{} {} {}".format(item[0], item[0], item[1]), sent)
        formatted_str = "\n".join(formatted_str_list)

        tree = self.execute(formatted_str, self._format_type_tagged, self._format_type_parsed)

        return tree

    def grammar(self):
        raise NotImplementedError()


def demo():
    freeling = FreeLing()
    tree = freeling.raw_parse(u"En el tramo de Telefónica, un toro descolgado ha creado peligro "
                              u"tras embestir contra un grupo de mozos.")
    tree[0].draw()


if __name__ == '__main__':
    demo()