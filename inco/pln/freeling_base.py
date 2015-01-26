# coding=utf-8
import os
import subprocess
import tempfile

__author__ = 'Matias'


class FreeLingBase:
    def _setup(self, path_to_tagger, verbose=False):
        self.verbose = verbose
        self.path_to_tagger = path_to_tagger
        if not os.path.isfile(path_to_tagger):
            raise Exception("No se encuentra ejecutable de FreeLing.")

    def execute(self, string, tokenized=False):
        if self.verbose:
            print "--- Creando archivos temporales ---"

        temp_input = tempfile.NamedTemporaryFile(delete=False, prefix="freeling_input_")
        temp_output = tempfile.NamedTemporaryFile(delete=False, prefix="freeling_output_")

        # escribir string a archivo temp de entrada
        temp_input.write(string.encode("utf-8"))

        output_name = temp_output.name
        input_name = temp_input.name

        temp_input.close()
        temp_output.close()

        if self.verbose:
            print "--- Ejecutando FreeLing ---"

        self.__execute_binary(self.path_to_tagger, input_name, output_name, tokenized=tokenized)

        if self.verbose:
            print "--- Procesando salida de FreeLing ---"

        result = self.process_output(output_name)

        if self.verbose:
            print "--- Borrando archivos temporales ---"

        os.remove(input_name)
        os.remove(output_name)

        return result

    def __execute_binary(self, tagger_path, input_file_path, output_file_path, tokenized=False):
        """
        Ejecuta FreeLing sobre un archivo, y escribe la salida en otro.
        """

        # la ejecucion es de la forma INPUT OUTPUT

        exe_name = "analyzer.exe"

        # verificar que la ruta del tagger pasada incluya el ejecutable, incluirlo si no esta
        # TODO windows / linux?

        execution_string = tagger_path
        if not execution_string.endswith(exe_name):
            execution_string = os.path.join(tagger_path, exe_name)

        bin_path = os.path.dirname(execution_string)

        if self.verbose:
            print "Ruta del binario: <" + bin_path + ">"

        cfg_path = os.path.join(bin_path, "analyzer.cfg")

        if self.verbose:
            print "Ruta de configuración: <" + bin_path + ">"

        if self.get_type() == FreeLingBase._type_parser:
            output_format_flag = 'parsed'
        elif self.get_type() == FreeLingBase._type_tagger:
            output_format_flag = 'tagged'
        else:
            output_format_flag = 'token'

        if tokenized:
            input_format_flag = 'token'
        else:
            input_format_flag = 'plain'

        execution_string += " -f " + cfg_path + " --lang es --inpf " + input_format_flag + " --outf " + output_format_flag

        execution_string += " <" + input_file_path
        execution_string += " >" + output_file_path

        if self.verbose:
            print "Ruta de ejecución: <" + execution_string + ">"

        res_code = subprocess.call(execution_string, shell=True)

        if self.verbose:
            print "Retorno de ejecución: " + str(res_code)

    _type_tokenizer = 'tokenizer'
    _type_parser = 'parser'
    _type_tagger = 'tagger'
