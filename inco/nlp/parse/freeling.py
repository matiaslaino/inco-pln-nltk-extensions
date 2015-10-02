# -*- coding: utf-8 -*-
import codecs
import os

from nltk import ParserI, TaggerI, word_tokenize

from inco.nlp.freeling_base import FreeLingBase
from inco.nlp.parse.tree.freeling_tree_builder import FreeLingTreeBuilder


__author__ = 'Matias Laino'


class FreeLing(FreeLingBase, ParserI):
    """
    Wrapper class for the FreeLing parser.
    """

    def __init__(self, path_to_executable=None, verbose=False, tagger=None):
        """
        Constructor.

        @param path_to_executable: path to the FreeLing executable
        @type path_to_executable: str
        @param tagger: POS-tagger to be used, in case tagging is required. Defaults to using FreeLing.
        @type tagger: nltk.tag.TaggerI
        @raise Exception: if executable is not found.
        """

        self.is_full = False
        self._initialize(path_to_executable, verbose)
        self._tagger = tagger

    def process_output(self, file_path):
        """
        Processes the complete output of FreeLing when configured as a parser.

        @param file_path: path to the output to process.
        @return: the processed parse tree.
        @rtype: nltk.tree.Tree
        """

        parse_tree_str = ""

        with codecs.open(file_path, encoding='utf8') as temp_output:
            for line in temp_output:
                parse_tree_str += line
                if self.verbose:
                    print(line)

        if self.verbose:
            print("FreeLing raw output: " + parse_tree_str)
            print("--- Building parse tree ---")

        tree_builder = FreeLingTreeBuilder()
        tree = tree_builder.build(parse_tree_str)

        return tree

    def raw_parse(self, sent, language='spanish'):
        """
        Parse a sentence using NLTK's word-tokenizer.
        Tokenization defaults to spanish.

        @param sent: The sentence to be parsed
        @type sent:unicode
        @rtype: iter(Tree)
        """

        tokens = word_tokenize(sent, language)
        return self.parse(tokens)

    def parse(self, sent, *args, **kwargs):
        """
        @return: An iterator that generates parse trees for the sentence.
        When possible this list is sorted from most likely to least likely.

        @param sent: The sentence to be parsed, tokenized
        @type sent: list(str)
        @rtype: iter(Tree)
        """

        formatted_str = "\n".join(sent)

        if self._tagger is not None and issubclass(type(self._tagger), TaggerI):
            tagged = self._tagger.tag(sent)
            iterator = self.tagged_parse(tagged)
        else:
            iterator = iter([self.execute(formatted_str, self._format_type_tokenized, self._format_type_parsed)])

        return iterator

    def tagged_parse(self, sent, verbose=False):
        """
        @return: An iterator that generates parse trees for the sentence.
        When possible this list is sorted from most likely to least likely.

        @param sent: The sentence to be parsed, tagged
        @type sent: list(str)
        @rtype: iter(Tree)
        """

        # the expected FreeLing format is:
        # word TAB lemma TAB pos_tag

        formatted_str_list = map(lambda item: u"{} {} {}".format(item[0], item[0], item[1]), sent)
        formatted_str = "\n".join(formatted_str_list)

        tree = self.execute(formatted_str, self._format_type_tagged, self._format_type_parsed)

        return iter([tree])

    def grammar(self):
        raise NotImplementedError()


def demo():
    freeling = FreeLing()
    tree = freeling.raw_parse(u"En el tramo de Telefónica, un toro descolgado ha creado peligro "
                              u"tras embestir contra un grupo de mozos.")
    next(tree).draw()


if __name__ == '__main__':
    demo()