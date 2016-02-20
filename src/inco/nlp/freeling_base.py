# coding=utf-8
import os
import subprocess
import tempfile

__author__ = 'Matias Laino'


class FreeLingBase:
    """
    Base class for FreeLing-based wrappers (tokenizer, tagger, parser).
    Contains initialization logic and basic code to invoke FreeLing.
    """

    def _initialize(self, path_to_tagger, verbose=False):
        """
        Initializes the FreeLing wrapper.
        """

        self.verbose = verbose
        self.path_to_tagger = path_to_tagger

        if self.path_to_tagger is None:
            self.path_to_tagger = os.environ['NLP_FREELING']

        if not os.path.isfile(self.path_to_tagger):
            raise Exception("FreeLing executable not found")

    def execute(self, input_str, input_format, output_format):
        """
        Invokes FreeLing.

        @param input_str: text upon which to invoke FreeLing.
        @type input_str: unicode
        @return: FreeLing\'s output, if successful.
        @rtype: str
        """

        # TODO: verbose output method?
        if self.verbose:
            print ("--- Creating temporal files ---")

        temp_input = tempfile.NamedTemporaryFile(delete=False, prefix="freeling_input_")
        temp_output = tempfile.NamedTemporaryFile(delete=False, prefix="freeling_output_")

        # save input string to a temporal file, so it can be supplied to FreeLing.
        temp_input.write(input_str.encode("utf-8"))

        output_name = temp_output.name
        input_name = temp_input.name

        temp_input.close()
        temp_output.close()

        if self.verbose:
            print("--- Executing FreeLing ---")

        # call the binary
        # todo: handle binary fail (res != 0)
        self.__execute_binary(self.path_to_tagger, input_name, output_name, input_format, output_format)

        if self.verbose:
            print("--- Processing FreeLing's output ---")

        # process the output. each derived class is responsible for doing this.
        # todo: unresolved reference warning, fix
        result = self.process_output(output_name)

        if self.verbose:
            print("--- Deleting temporal files ---")

        os.remove(input_name)
        os.remove(output_name)

        return result

    def __execute_binary(self, tagger_path, input_file_path, output_file_path, input_format, output_format):
        """
        Executes FreeLing on an input file, and writes the output in another file.
        @param tagger_path:
        @param input_file_path:
        @param output_file_path:
        @return: binary result code
        @rtype : int

        """

        # FreeLing expects invokation in the form of "EXECUTABLE_FILE_PATH INPUT_FILE_PATH OUTPUT_FILE_PATH"
        exe_name = "analyzer.exe"

        # verificar que la ruta del tagger pasada incluya el ejecutable, incluirlo si no esta
        # TODO windows / linux?

        # todo: this might not be necessary, and is probably breaking for linux/mac
        execution_string = tagger_path
        if not execution_string.endswith(exe_name):
            execution_string = os.path.join(tagger_path, exe_name)

        bin_path = os.path.dirname(execution_string)

        if self.verbose:
            print("Binary path: <" + bin_path + ">")

        # we are expecting the configuration file to be on the same directory as the executable
        cfg_path = os.path.join(bin_path, "analyzer.cfg")

        if self.verbose:
            print("Configuration path: <" + bin_path + ">")

        # assemble execution string
        execution_string += " -f {0} --lang es --inpf {1} --outf {2}".format(cfg_path, input_format,
                                                                             output_format)

        execution_string += " <" + input_file_path
        execution_string += " >" + output_file_path

        if self.verbose:
            print("Execution string: <" + execution_string + ">")

        res_code = subprocess.call(execution_string, shell=True)

        if self.verbose:
            print("Execution result: " + str(res_code))

        return res_code

    _type_tokenizer = 'tokenizer'
    _type_parser = 'parser'
    _type_tagger = 'tagger'

    _format_type_plain = 'plain'
    _format_type_tokenized = 'token'
    _format_type_tagged = 'tagged'
    _format_type_parsed = 'parsed'
    _format_type_sense = 'sense'

