import codecs
import os
import tempfile
import subprocess

from nltk import ParserI, word_tokenize, TaggerI, Tree

__author__ = 'Matias Laino'


class StanfordShiftReduceParser(ParserI):
    """
    Wrapper class for the Stanford Shift-Reduce parser.
    """

    def __init__(self, path_to_jar=None, path_to_model=None, tagger=None):
        """
        Constructor.

        @param path_to_jar: path to the Stanford Parser JAR file.
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
            self.path_to_jar = os.environ['NLP_STANFORDSR']

        if self.path_to_model is None:
            self.path_to_model = os.environ['NLP_STANFORDSR_MODEL']

        """@type : nltk.tag.TaggerI"""
        self.tagger = tagger

        if not os.path.isfile(self.path_to_jar):
            raise Exception("Stanford SR JAR not found.")
        if not os.path.isfile(self.path_to_model):
            raise Exception("Stanford SR model file not found")

    def raw_parse(self, sent, language='spanish'):
        """
        Parse a sentence using NLTK's word-tokenizer.
        Tokenization defaults to spanish.

        @param sent: The sentence to be parsed
        @type sent:str
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
        Parses an already tagged sentence

        @param sent: sentence to be parsed, tokenized and tagged
        @type sent:list(tuple(str, str))
        @return:
        """

        str_result = u''
        for item in sent:
            word = item[0]
            tag = item[1]

            str_result += u"{}/{}\n".format(word, tag)

        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_output = tempfile.NamedTemporaryFile(delete=False)

        temp_input.write(str_result.encode('utf-8'))

        temp_input.close()
        temp_output.close()

        output_name = temp_output.name
        input_name = temp_input.name

        if verbose:
            print ("--- Executing Stanford SR Parser ---")

        res_code = self.__execute(input_name, output_name)

        # cmd = [
        #     'StanfordSRBinding',
        #     '-model', 'edu/stanford/nlp/models/srparser/spanishSR.ser.gz',
        #     '-sentences', 'newline',
        #     '-outputFormat', 'penn',
        #     '-tokenized',
        #     '-tagSeparator', '/',
        #     '-tokenizerFactory', 'edu.stanford.nlp.process.WhitespaceTokenizer',
        #     '-tokenizerMethod', 'newCoreLabelTokenizerFactory',
        # ]

        # dirname = os.path.dirname(os.path.abspath(__file__))
        # stdout, stderr = java(cmd, classpath=(self.path_to_jar.encode('ascii','ignore'), self.path_to_model.encode('ascii','ignore'), dirname.encode('ascii','ignore')),
        #                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stdout = stdout.decode('utf8')

        if verbose:
            print ("Stanford result code: " + str(res_code))

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
            print ("Stanford SR raw output: \n" + parse_tree_str)
            print ("--- Building parse tree ---")

        tree = Tree.fromstring(parse_tree_str)

        return iter([tree])

    def __execute(self, input_path, output_path):
        dir_name = os.path.dirname(os.path.abspath(__file__))

        cmd = 'java -Xms1024m -cp {};{};{};.;* StanfordSRBinding -model edu/stanford/nlp/models/srparser/spanishSR.ser.gz -input {} -output {}' \
            .format(self.path_to_jar, self.path_to_model, dir_name, input_path, output_path)

        return self.__execute_binary(cmd)

    @staticmethod
    def __execute_binary(cmd, verbose=False):
        output = None if verbose else subprocess.PIPE

        p = subprocess.Popen(cmd, stdout=output, stderr=output)
        return p.wait()


def demo():
    # previously tagged by FreeLing
    tokens = [(u'En', u'SPS00'), (u'el', u'DA0MS0'), (u'tramo', u'NCMS000'), (u'de', u'SPS00'),
          (u'Telef\xf3nica', u'NP00000'), (u',', u'Fc'), (u'un', u'DI0MS0'),
          (u'toro', u'NCMS000'), (u'descolgado', u'VMP00SM'), (u'ha', u'VAIP3S0'),
          (u'creado', u'VMP00SM'), (u'peligro', u'NCMS000'), (u'tras', u'SPS00'),
          (u'embestir', u'VMN0000'), (u'contra', u'SPS00'), (u'un', u'DI0MS0'),
          (u'grupo', u'NCMS000'), (u'de', u'SPS00'), (u'mozos', u'NCMP000'), (u'.', u'Fp')]

    parser = StanfordShiftReduceParser()
    parser.tagged_parse(tokens, verbose=True)[0].draw()

if __name__ == '__main__':
    demo()