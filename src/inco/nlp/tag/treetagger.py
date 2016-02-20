# -*- coding: utf8 -*-
from nltk import TaggerI, word_tokenize
from nltk.tokenize.api import TokenizerI

from inco.nlp.tag.convert.tag_converter import TreeTaggerConverter


__author__ = 'Matias Laino'

import re
import tempfile
import os
import subprocess
import inco.nlp.tagging_constants as constants


class TreeTagger(TaggerI):
    """
    Wrapper class for TreeTagger
    """

    def __init__(self, path_to_tagger=None, tokenizer=None):
        """
        Constructor.

        :parameter path_to_tagger: path to binary
        @type path_to_tagger: str
        @param tokenizer: tokenizer to be used prior to tagging
        @type tokenizer: TokenizerI
        """

        self.tagger_path = path_to_tagger

        if self.tagger_path is None:
            self.tagger_path = os.environ['NLP_TREETAGGER']

        self.__processor = TreeTagger.__process
        if not os.path.isfile(self.tagger_path):
            raise Exception("TreeTagger executable not found")

        self.__tokenizer = tokenizer

    def tag(self, sent):
        """
        Tags a collection of tokens.

        @param sent: the collection of tokens to POS tag.
        @type sent: list(str)
        @return: the collection of tokens, POS tagged. Each entry contains: WORD POS-TAG
        @rtype: list(tuple(str, str))
        """

        self.__processor = TreeTagger.__process
        string = "\n".join(sent)
        return self.__execute(string)

    def tag_native(self, sent):
        """
        Tags a collection of tokens using the tagger's native tags.

        @param tokens: the collection of tokens to POS tag.
        @type tokens: list(str)
        @return: the collection of tokens, POS tagged. Each entry contains: WORD POS-TAG
        @rtype: list(tuple(str, str))
        """

        string = "\n".join(sent)
        self.__processor = TreeTagger.__process_native
        return self.__execute(string)

    def tag_full(self, sent):
        """
        Tags a collection of tokens.

        @param tokens: the collection of tokens to POS tag.
        @type tokens: list(str)
        @return: the collection of tokens, POS tagged. Each entry contains: WORD LEMMA COARSE-TAG POS-TAG FEATURES
        @rtype: list(dict)
        """

        string = "\n".join(sent)
        self.__processor = TreeTagger.__process_full
        self.__execute(string)

    def raw_tag(self, sent):
        """

        @param sent:
        @type sent:str
        @return:
        """
        if self.__tokenizer is not None:
            tokens = self.__tokenizer.tokenize(sent)
        else:
            tokens = word_tokenize(sent, 'spanish')

        self.__processor = TreeTagger.__process
        return self.tag(tokens)

    def raw_tag_full(self, string):
        """
        Tags a string.

        @param string: string to POS tag.
        @type string: str
        @return: the collection of tokens, POS tagged. Each entry contains: WORD LEMMA COARSE-TAG POS-TAG FEATURES
        @rtype: list(dict)
        """

        if self.__tokenizer is not None:
            tokens = self.__tokenizer.tokenize(string)
        else:
            tokens = word_tokenize(string)

        string = "\n".join(tokens)
        self.__processor = TreeTagger.__process_full
        return self.__execute(string)

    def __execute(self, string):
        result = []

        temp_input = tempfile.NamedTemporaryFile(delete=False, prefix='treetagger_input_')
        temp_output = tempfile.NamedTemporaryFile(delete=False, prefix='treetagger_output_')

        # write input string to a temporary file
        temp_input.write(string.encode("utf-8"))

        output_name = temp_output.name
        input_name = temp_input.name

        temp_input.close()
        temp_output.close()

        # execute TreeTagger
        TreeTagger.__execute_binary(self.tagger_path, input_name, output_name)

        # process tagger output
        with open(output_name) as output_file:
            for line in output_file:
                tagged_dict = TreeTagger.__convert_line(line)
                result.append(self.__processor(tagged_dict))

        os.remove(input_name)
        os.remove(output_name)

        return result

    @staticmethod
    def __execute_binary(tagger_path, input_file_path, output_file_path):
        """
        Executes TreeTagger binary.
        @return: binary result code
        @rtype: int
        """

        # todo: this may not be necessary
        bat_name = "tag-spanish.bat"

        # TODO windows / linux?

        execution_string = tagger_path
        if not execution_string.endswith(bat_name):
            execution_string = os.path.join(tagger_path, bat_name)

        execution_string += " " + input_file_path
        execution_string += " " + output_file_path

        print(execution_string)

        res_code = subprocess.call(execution_string)

        return res_code

    @staticmethod
    def __process_full(tagged_dict):
        return dict([(constants.WORD, tagged_dict[constants.WORD]),
                     (constants.LEMMA, tagged_dict[constants.LEMMA]),
                     (constants.COARSE_TAG, tagged_dict[constants.COARSE_TAG]),
                     (constants.POS_TAG, tagged_dict[constants.POS_TAG]),
                     (constants.FEATURES, dict([
                         (constants.TAGGER, constants.TAGGERS_TREETAGGER),
                         (constants.ORIGINAL_TAG, tagged_dict[constants.ORIGINAL_TAG])
                     ]))])

    @staticmethod
    def __process_native(tagged_dict):
        return tagged_dict[constants.WORD], tagged_dict[constants.ORIGINAL_TAG]

    @staticmethod
    def __process(tagged_dict):
        return tagged_dict[constants.WORD], tagged_dict[constants.POS_TAG]

    @staticmethod
    def __convert_line(input_line):
        """
        Converts a single line of TreeTagger output into a dictionary.

        dictionary keys:
            word
            lemma
            original_tag
            coarse_tag
            pos_tag

        @param input_line: line to convert from FreeLing format to a dictionary.
        @type input_line: str
        @return the FreeLing output line, formatted into a dictionary
        @rtype: dict
        """

        # form: word, lemma, coarse tag, pos tag, original tag
        tree_tagger_regular_expression = re.compile("^(.*)?\t(.*)?\t(.*)?$")

        utf8line = input_line
        parsed_line = tree_tagger_regular_expression.match(utf8line)

        tags = TreeTaggerConverter.convert_tag(parsed_line.group(2), parsed_line.group(1))

        result_object = {constants.WORD: parsed_line.group(1), constants.LEMMA: parsed_line.group(3),
                         constants.ORIGINAL_TAG: parsed_line.group(2),
                         constants.COARSE_TAG: tags[0], constants.POS_TAG: tags[1]}

        return result_object


def demo():
    tagger = TreeTagger()
    tagged = tagger.raw_tag(u"En el tramo de Telefónica, un toro descolgado ha creado peligro "
                            u"tras embestir contra un grupo de mozos.")
    print(tagged)


if __name__ == '__main__':
    demo()


