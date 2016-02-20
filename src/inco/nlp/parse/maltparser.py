# -*- coding: utf-8 -*-
import codecs
import subprocess
import tempfile
import os

from nltk import ParserI, word_tokenize, TaggerI

from inco.nlp.parse.tree.maltparser_tree_builder import MaltParserTreeBuilder


__author__ = 'Matias Laino'


class MaltParser(ParserI):
    """
    Wrapper class for MaltParser.
    """

    def __init__(self, path_to_jar=None, path_to_model=None, tagger=None):
        """
        Constructor.

        @param path_to_jar: path to the MaltParser JAR file.
        @type path_to_jar: str
        @param path_to_model: path to the Stanford model file.
        @type path_to_model: str
        @param tagger: POS-tagger to be used, in case tagging is required. Parser will fail if None is passed and is later required
        @type tagger: nltk.tag.TaggerI
        @raise Exception: If JAR or model files are not found.
        """

        self.path_to_model = path_to_model
        self.path_to_jar = path_to_jar

        if self.path_to_jar is None:
            self.path_to_jar = os.environ['NLP_MALTPARSER']

        if self.path_to_model is None:
            self.path_to_model = os.environ['NLP_MALTPARSER_MODEL']

        """@type : nltk.tag.TaggerI"""
        self.tagger = tagger

        if not os.path.isfile(self.path_to_jar):
            raise Exception("MaltParser JAR not found.")
        if not os.path.isfile(self.path_to_model):
            raise Exception("MaltParser model file not found")

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

        if self.tagger is None or issubclass(type(self.tagger), TaggerI) is False:
            raise Exception("Tagger not set, cannot parse raw tokens without their tags")

        tagged_sent = self.tagger.tag(sent)
        return self.tagged_parse(tagged_sent)

    def tagged_parse(self, sent, verbose=False):
        """
        @return: An iterator that generates parse trees for the sentence.
        When possible this list is sorted from most likely to least likely.

        @param sent: The sentence to be parsed, tagged
        @type sent: list(str)
        @rtype: iter(Tree)
        """

        str_result = u''
        i = 1
        for item in sent:
            word = item[0]
            tag = item[1]

            str_result += u"{}\t{}\t{}\t{}\t{}\t_\t_\t_\t_\t_\n".format(repr(i), word, "_", tag, tag)
            i += 1

        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_output = tempfile.NamedTemporaryFile(delete=False)

        temp_input.write(str_result.encode('utf-8'))

        temp_input.close()
        temp_output.close()

        output_name = temp_output.name
        input_name = temp_input.name

        if verbose:
            print("--- Executing MaltParser ---")

        res_code = self.__execute(input_name, output_name)

        if verbose:
            print ("MaltParser result code: " + str(res_code))

        parse_tree_str = ""

        with codecs.open(output_name, encoding='utf8') as temp_output:
            for line in temp_output:
                if line != "" and line != "\n":
                    parse_tree_str += line

        if verbose:
            print ("--- Deleting temporal files ---")

        os.remove(input_name)
        os.remove(output_name)

        if verbose:
            print ("Maltparser raw output: \n" + parse_tree_str)
            print ("--- Building parse tree ---")

        tree_builder = MaltParserTreeBuilder()
        tree = tree_builder.build(parse_tree_str)

        return iter([tree])

    def __execute(self, input_file_path, output_file_path, verbose=False):
        """
        Executes MaltParser.

        @param input_file_path: input file path
        @type input_file_path: str
        @param output_file_path: destination output file path
        @type output_file_path: str
        @param verbose: indicates if additional information is outputted
        @type verbose: bool
        @return: MaltParser return
        """

        model_working_dir = os.path.dirname(self.path_to_model)
        model_name = os.path.basename(self.path_to_model)

        command = "java -Xmx1024m -jar {} -w {} -c {} -i {} -o {} -m parse".format(self.path_to_jar, model_working_dir,
                                                                                   model_name,
                                                                                   input_file_path, output_file_path)

        if verbose:
            print("Execution string: <" + command + ">")

        # print command
        return MaltParser.__execute_binary(command, verbose)

    @staticmethod
    def __execute_binary(cmd, verbose=False):
        output = None if verbose else subprocess.PIPE
        p = subprocess.Popen(cmd, stdout=output, stderr=output)
        return p.wait()

    def grammar(self):
        pass


def demo():
    # previously tagged by FreeLing
    tokens = [(u'En', u'SPS00'), (u'el', u'DA0MS0'), (u'tramo', u'NCMS000'), (u'de', u'SPS00'),
              (u'Telef\xf3nica', u'NP00000'), (u',', u'Fc'), (u'un', u'DI0MS0'),
              (u'toro', u'NCMS000'), (u'descolgado', u'VMP00SM'), (u'ha', u'VAIP3S0'),
              (u'creado', u'VMP00SM'), (u'peligro', u'NCMS000'), (u'tras', u'SPS00'),
              (u'embestir', u'VMN0000'), (u'contra', u'SPS00'), (u'un', u'DI0MS0'),
              (u'grupo', u'NCMS000'), (u'de', u'SPS00'), (u'mozos', u'NCMP000'), (u'.', u'Fp')]

    parser = MaltParser()
    parser.tagged_parse(tokens)[0].draw()


if __name__ == '__main__':
    demo()