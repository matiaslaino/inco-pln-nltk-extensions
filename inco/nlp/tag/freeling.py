# coding=utf-8
import re

from inco.nlp.freeling_base import FreeLingBase


__author__ = 'Matias Laino'

from nltk import TaggerI
import inco.nlp.tagging_constants as constants


class FreeLing(FreeLingBase, TaggerI):
    """
    Wrapper class for the FreeLing tagger.
    """

    def __init__(self, path_to_tagger=None, verbose=False):
        """
        Constructor.

        @param path_to_tagger: path to the FreeLing executable
        @type path_to_tagger: str
        """
        self._initialize(path_to_tagger, verbose)
        self.__processor = FreeLing.__process_native

    @staticmethod
    def __process_full(tagged_dict):
        # todo: add each dictionary directly...
        return dict([(constants.WORD, tagged_dict[constants.WORD]),
                     (constants.LEMMA, tagged_dict[constants.LEMMA]),
                     (constants.COARSE_TAG, tagged_dict[constants.COARSE_TAG]),
                     (constants.POS_TAG, tagged_dict[constants.POS_TAG]),
                     (constants.FEATURES, dict([
                         (constants.TAGGER, constants.TAGGERS_FREELING),
                         (constants.PROBABILITY, tagged_dict[constants.PROBABILITY])
                     ]))])

    @staticmethod
    def __process_native(tagged_dict):
        return tagged_dict[constants.WORD], tagged_dict[constants.POS_TAG]

    def process_output(self, file_path):
        """
        Processes the complete output of FreeLing when configured as a tagger.

        @param file_path: path to the output to process.
        @type file_path: str
        @return: the list of tagged tokens, each one as a dictionary containing information on the token.
        @rtype: list(dict)
        """

        result = []

        with open(file_path) as output_file:
            for line in output_file:
                if self.verbose:
                    print ("Raw FreeLing output: " + line)

                if line != "\n":
                    converted_line = FreeLing.__convert_line(line)
                    result.append(self.__processor(converted_line))

        return result

    def tag(self, tokens):
        """
        Tags a collection of tokens.

        @param tokens: the collection of tokens to POS tag.
        @type tokens: list(str)
        @return: the collection of tokens, POS tagged. Each entry contains: WORD POS-TAG
        @rtype: list(tuple(str, str))
        """
        string = "\n".join(tokens)
        self.__processor = FreeLing.__process_native
        return self.execute(string, self._format_type_tokenized, self._format_type_tagged)

    def native_tag(self, tokens):
        """
        Tags a collection of tokens using the tagger's native tags.
        This method is available for consistency with other taggers, in the case of FreeLing it is equivalent
        to calling tag()

        @param tokens: the collection of tokens to POS tag.
        @type tokens: list(str)
        @return: the collection of tokens, POS tagged. Each entry contains: WORD POS-TAG
        @rtype: list(tuple(str, str))
        """

        return self.tag(tokens)

    def tag_full(self, tokens):
        """
        Tags a collection of tokens.

        @param tokens: the collection of tokens to POS tag.
        @type tokens: list(str)
        @return: the collection of tokens, POS tagged. Each entry contains: WORD LEMMA COARSE-TAG POS-TAG FEATURES
        @rtype: list(dict)
        """

        self.__processor = FreeLing.__process_full
        string = "\n".join(tokens)
        return self.execute(string, self._format_type_tokenized, self._format_type_tagged)

    def raw_tag(self, sent):
        """
        Tags an untokenized sentence.

        @param sent: sentence to be tokenized and tagged
        @type sent: unicode
        @return: the collection of tokens, POS tagged. Each entry contains: WORD POS-TAG
        @rtype: list(tuple(str, str))
        """

        self.__processor = FreeLing.__process_native
        return self.execute(sent, self._format_type_plain, self._format_type_tagged)

    def raw_tag_full(self, string):
        """
        Tags a collection of tokens.

        @param string: string to POS tag.
        @type string: unicode
        @return: the collection of tokens, POS tagged. Each entry contains: WORD LEMMA COARSE-TAG POS-TAG FEATURES
        @rtype: list(dict)
        """

        self.__processor = FreeLing.__process_full
        return self.execute(string, self._format_type_plain, self._format_type_tagged)

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

        @param input_line: line to convert from FreeLing format to a dictionary.
        @type input_line: str
        @return the FreeLing output line, formatted into a dictionary
        @rtype: dict

        """
        # regular expression to recognize: word lemma coarse-tag pos-tag original-tag
        tree_tagger_regular_expression = re.compile("^(.*)? (.*)? (.*)? (.*)?")

        utf8line = input_line
        parsed_line = tree_tagger_regular_expression.match(utf8line)

        result_object = {constants.WORD: parsed_line.group(1), constants.LEMMA: parsed_line.group(2),
                         constants.ORIGINAL_TAG: parsed_line.group(3),
                         constants.COARSE_TAG: parsed_line.group(3)[0], constants.POS_TAG: parsed_line.group(3),
                         constants.PROBABILITY: parsed_line.group(4)}

        return result_object


def demo():
    freeling = FreeLing()
    tagged = freeling.raw_tag(u"En el tramo de Telefónica, un toro descolgado ha creado peligro "
                              u"tras embestir contra un grupo de mozos.")
    print (tagged)


if __name__ == '__main__':
    demo()