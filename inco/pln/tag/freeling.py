# coding=utf-8
import os
import subprocess
import tempfile
import re

__author__ = 'Matias'

from nltk import TaggerI
import inco.pln.tagging_constants as constants


class FreeLing(TaggerI):
    def __init__(self, path_to_tagger):
        self.path_to_tagger = path_to_tagger
        if not os.path.isfile(path_to_tagger):
            raise Exception("No se encuentra ejecutable de FreeLing.")


    def tag(self, tokens, verbose=False):
        return self.__tag_custom(tokens, False, verbose)

    def tag_full(self, tokens, verbose=False):
        string = "\n".join(tokens)
        return self.__tag_custom(string, True, verbose, tokenized=True)

    def tag_string_full(self, string, verbose=False):
        return self.__tag_custom(string, True, verbose, tokenized=True)

    def __tag_custom(self, string, is_full, verbose=False, tokenized=False):
        result = []

        if verbose:
            print "--- Creando archivos temporales ---"

        temp_input = tempfile.NamedTemporaryFile(delete=False)
        temp_output = tempfile.NamedTemporaryFile(delete=False)

        # escribir string a archivo temp de entrada
        temp_input.write(string.encode("utf-8"))

        output_name = temp_output.name
        input_name = temp_input.name

        temp_input.close()
        temp_output.close()

        if verbose:
            print "--- Ejecutando FreeLing ---"

        FreeLing.__execute(self.path_to_tagger, input_name, output_name, tokenized=tokenized)

        if verbose:
            print "--- Procesando salida de FreeLing ---"

        # hay que procesar el archivo leido, hay que leerlo primero.
        with open(output_name) as output_file:
            for line in output_file:
                if verbose:
                    print "Salida de FreeLing: " + line

                if line != "\n":
                    converted_line = FreeLing.__convert_line(line)

                    if is_full:
                        result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                            (constants.LEMMA, converted_line[constants.LEMMA]),
                                            (constants.COARSE_TAG, converted_line[constants.COARSE_TAG]),
                                            (constants.POS_TAG, converted_line[constants.POS_TAG]),
                                            (constants.FEATURES, dict([
                                                (constants.TAGGER, constants.TAGGERS_FREELING),
                                                (constants.PROBABILITY, converted_line[constants.PROBABILITY])
                                            ]))]))
                    else:
                        result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                            (constants.ORIGINAL_TAG, converted_line[constants.ORIGINAL_TAG])]))

        if verbose:
            print "--- Borrando archivos temporales ---"

        os.remove(input_name)
        os.remove(output_name)

        return result

    @staticmethod
    def __execute(tagger_path, input_file_path, output_file_path, verbose=False, tokenized=False):
        """
        Ejecuta el tagger sobre un archivo, y escribe la salida en otro.
        """

        # la ejecucion es de la forma INPUT OUTPUT

        exe_name = "analyzer.exe"

        # verificar que la ruta del tagger pasada incluya el ejecutable, incluirlo si no esta
        # TODO windows / linux?

        execution_string = tagger_path
        if not execution_string.endswith(exe_name):
            execution_string = os.path.join(tagger_path, exe_name)

        bin_path = os.path.dirname(execution_string)

        if verbose:
            print "Ruta del binario: <" + bin_path + ">"

        cfg_path = os.path.join(bin_path, "analyzer.cfg")

        if verbose:
            print "Ruta de configuración: <" + bin_path + ">"

        if tokenized:
            input_format_flag = 'tokenized'
        else:
            input_format_flag = 'plain'

        execution_string += " -f " + cfg_path + " --lang es --inpf " + input_format_flag + " --outf tagged"

        execution_string += " <" + input_file_path
        execution_string += " >" + output_file_path

        if verbose:
            print "Ruta de ejecución: <" + execution_string + ">"

        res_code = subprocess.call(execution_string, shell=True)

        if verbose:
            print "Retorno de ejecución: " + str(res_code)

    @staticmethod
    def __convert_line(input_line):
        """
        Convierte una linea de output de TreeTagger a un diccionario.

        claves del diccionario:
            word
            lemma
            original_tag
            coarse_tag
            pos_tag
            probability
        """
        # forma: palabra, lemma, coarse tag, pos tag, original tag
        tree_tagger_regular_expression = re.compile("^(.*)? (.*)? (.*)? (.*)?")

        utf8line = input_line.decode('utf8')
        parsed_line = tree_tagger_regular_expression.match(utf8line)
        # print utf8line
        result_object = {constants.WORD: parsed_line.group(1), constants.LEMMA: parsed_line.group(2),
                         constants.ORIGINAL_TAG: parsed_line.group(3),
                         constants.COARSE_TAG: parsed_line.group(3)[0], constants.POS_TAG: parsed_line.group(3),
                         constants.PROBABILITY: parsed_line.group(4)}

        return result_object
