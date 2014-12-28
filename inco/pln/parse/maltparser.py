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
    def __init__(self, path_to_jar, path_to_model):
        self.path_to_model = path_to_model
        self.path_to_jar = path_to_jar

        if not os.path.isfile(path_to_jar):
            raise Exception("No se encuentra JAR de MaltParser.")
        if not os.path.isfile(path_to_model):
            raise Exception("No se encuentra modelo para el Español de MaltParser.")

    def parse(self, sent_str, verbose=False):
        # traducir desde nuestro formato esperado al formato de entrada de MaltParser.
        # nuestro formato es un diccionario.
        # El formato de entrada de MaltParser es:
        # numero_token     palabra     lemma       coarse_tag      pos_tag     _   _   _   _   _

        utf8_line = sent_str.decode('utf8')
        line = json.loads(utf8_line)

        i = 1

        str_result = u''

        if verbose:
            print "--- Procesando tokens de entrada  ---"

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
            print "--- Creando archivos temporales ---"

        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_output = tempfile.NamedTemporaryFile(delete=False)

        temp_input.write(str_result.encode('utf-8'))

        temp_input.close()
        temp_output.close()

        output_name = temp_output.name
        input_name = temp_input.name

        if verbose:
            print "--- Archivos temporales creados ---"

        res_code = self.__execute(input_name, output_name)

        if verbose:
            print "Código retorno MaltParser: " + str(res_code)

        parse_tree_str = ""

        with codecs.open(output_name, encoding='utf8') as temp_output:
            for line in temp_output:
                if line != "" and line != "\n":
                    parse_tree_str += line

        if verbose:
            print "--- Borrando archivos temporales ---"

        os.remove(input_name)
        os.remove(output_name)

        if verbose:
            print "Salida de MaltParser: \n" + parse_tree_str
            print "--- Construyendo árbol de parseo ---"

        tree_builder = MaltParserTreeBuilder()
        tree = tree_builder.build(parse_tree_str)

        return tree

    def __execute(self, input_file_path, output_file_path, verbose=False):
        model_working_dir = os.path.dirname(self.path_to_model)
        model_name = os.path.basename(self.path_to_model)

        command = "java -Xmx1024m -jar {} -w {} -c {} -i {} -o {} -m parse".format(self.path_to_jar, model_working_dir,
                                                                                   model_name,
                                                                                   input_file_path, output_file_path)

        if verbose:
            print "Comando: <" + command + ">"

        # print command
        return MaltParser._execute(command, verbose)

    @staticmethod
    def _execute(cmd, verbose=False):
        output = None if verbose else subprocess.PIPE
        p = subprocess.Popen(cmd, stdout=output, stderr=output)
        return p.wait()