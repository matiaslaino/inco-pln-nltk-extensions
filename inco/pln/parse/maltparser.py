# -*- coding: utf-8 -*-
import codecs
import json
import subprocess
import tempfile
import os

from nltk import ParserI

from inco.pln.parse.tree.maltparser_tree_builder import MaltParserTreeBuilder
import inco.pln.tagging_constants as constants


__author__ = 'Matias'


class MaltParser(ParserI):
    """
    MaltParser wrapper.
    """

    def __init__(self, path_to_jar, path_to_model):
        """
        Constructor.

        :param path_to_jar: path to the MaltParser JAR file.
        :type path_to_jar: str
        :param path_to_model: path to the MaltParser model file (.mco).
        :type path_to_model: str
        :raise Exception: if MaltParser JAR or model files are not found.
        """

        self.path_to_model = path_to_model
        self.path_to_jar = path_to_jar

        if not os.path.isfile(path_to_jar):
            raise Exception("No se encuentra JAR de MaltParser.")
        if not os.path.isfile(path_to_model):
            raise Exception("No se encuentra modelo para el Español de MaltParser.")

    def parse(self, input_str, verbose=False):
        """
        Entry point for MaltParser.
        Converts the input string, from our own format, to the expected format of MaltParser.

        :param input_str: input string
        :type input_str: str
        :param verbose: indicate if additional output will be sent to standard output.
        :return: the processed parse tree.
        :rtype: nltk.tree.Tree
        """

        # the expected MaltParser format is:
        # token_number TAB word TAB lemma TAB coarse_tag TAB pos_tag TAB _ TAB _ TAB _ TAB _ TAB _
        # our internal format is a dictionary saved as json.

        utf8_line = input_str.decode('utf8')
        line = json.loads(utf8_line)

        i = 1

        str_result = u''

        if verbose:
            print "--- Processing input ---"

        try:
            for word_dict in line:
                str_result += u"{}\t{}\t{}\t{}\t{}\t_\t_\t_\t_\t_\n".format(repr(i), word_dict[constants.WORD],
                                                                            word_dict[constants.LEMMA],
                                                                            word_dict[constants.COARSE_TAG],
                                                                            word_dict[constants.POS_TAG])
                i += 1
        except KeyError, e:
            print e
            exit()

        if verbose:
            print "--- Creating temporal files ---"

        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_output = tempfile.NamedTemporaryFile(delete=False)

        temp_input.write(str_result.encode('utf-8'))

        temp_input.close()
        temp_output.close()

        output_name = temp_output.name
        input_name = temp_input.name

        if verbose:
            print "--- Executing MaltParser ---"

        res_code = self.__execute(input_name, output_name)

        if verbose:
            print "MaltParser result code: " + str(res_code)

        parse_tree_str = ""

        with codecs.open(output_name, encoding='utf8') as temp_output:
            for line in temp_output:
                if line != "" and line != "\n":
                    parse_tree_str += line

        if verbose:
            print "--- Deleting temporal files ---"

        os.remove(input_name)
        os.remove(output_name)

        if verbose:
            print "Maltparser raw output: \n" + parse_tree_str
            print "--- Building parse tree ---"

        tree_builder = MaltParserTreeBuilder()
        tree = tree_builder.build(parse_tree_str)

        return tree

    def __execute(self, input_file_path, output_file_path, verbose=False):
        """
        Executes MaltParser.

        :param input_file_path: input file path
        :type input_file_path: str
        :param output_file_path: destination output file path
        :type output_file_path: str
        :param verbose: indicates if additional information is outputted
        :type verbose: bool
        :return: MaltParser return
        """

        model_working_dir = os.path.dirname(self.path_to_model)
        model_name = os.path.basename(self.path_to_model)

        command = "java -Xmx1024m -jar {} -w {} -c {} -i {} -o {} -m parse".format(self.path_to_jar, model_working_dir,
                                                                                   model_name,
                                                                                   input_file_path, output_file_path)

        if verbose:
            print "Execution string: <" + command + ">"

        # print command
        return MaltParser._execute(command, verbose)

    @staticmethod
    def _execute(cmd, verbose=False):
        output = None if verbose else subprocess.PIPE
        p = subprocess.Popen(cmd, stdout=output, stderr=output)
        return p.wait()

    def grammar(self):
        pass