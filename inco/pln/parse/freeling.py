# -*- coding: utf-8 -*-
import codecs

import json
import subprocess
import tempfile
import os

from nltk import ParserI

import inco.pln.tagging_constants as constants
from inco.pln.parse.tree.freeling_tree_builder import FreeLingTreeBuilder

__author__ = 'Matias'


class FreeLing(ParserI):
    def __init__(self, path_to_freeling):
        self.path_to_freeling = path_to_freeling

        if not os.path.isfile(path_to_freeling):
            raise Exception("No se encuentra ejecutable de FreeLing.")

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

        if verbose:
            print "--- Creando archivos temporales ---"

        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_output = tempfile.NamedTemporaryFile(delete=False)

        temp_input.write(str_result.encode('utf-8'))

        temp_input.close()
        temp_output.close()

        output_name = temp_output.name
        input_name = temp_input.name

        res_code = self.__execute(input_name, output_name)

        if verbose:
            print "Código de retorno de Freeling: " + str(res_code)

        parse_tree_str = ""

        with codecs.open(output_name, encoding='utf8') as temp_output:
            for line in temp_output:
                parse_tree_str += line
                if verbose:
                    print line

        if verbose:
            print "Salida de FreeLing: " + parse_tree_str
            print "--- Creando árbol de parseo ---"

        if verbose:
            print "--- Eliminando archivos temporales ---"

        os.remove(input_name)
        os.remove(output_name)

        if verbose:
            print "--- Construyendo árbol de parseo ---"

        tree_builder = FreeLingTreeBuilder()
        tree = tree_builder.build(parse_tree_str)

        return tree

    def __execute(self, input_file_path, output_file_path, verbose=False):
        """
        Ejecuta el tagger sobre un archivo, y escribe la salida en otro.
        """

        # la ejecucion es de la forma INPUT OUTPUT

        exe_name = "analyzer.exe"

        # verificar que la ruta del tagger pasada incluya el ejecutable, incluirlo si no esta
        # TODO windows / linux?

        execution_string = self.path_to_freeling
        if not execution_string.endswith(exe_name):
            execution_string = os.path.join(execution_string, exe_name)

        bin_path = os.path.dirname(execution_string)

        if verbose:
            print "Ruta del binario: <" + bin_path + ">"

        cfg_path = os.path.join(bin_path, "analyzer.cfg")

        if verbose:
            print "Ruta de configuración: <" + bin_path + ">"

        execution_string += " -f " + cfg_path + " --lang es --inpf tagged --outf parsed"

        execution_string += " <" + input_file_path
        execution_string += " >" + output_file_path

        if verbose:
            print "Ruta de ejecución: <" + execution_string + ">"

        res_code = subprocess.call(execution_string, shell=True)

        if verbose:
            print "Retorno de ejecución: " + str(res_code)

        return res_code