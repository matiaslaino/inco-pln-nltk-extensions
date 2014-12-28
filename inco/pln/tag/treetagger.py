# -*- coding: utf8 -*-
from nltk import TaggerI

__author__ = 'Matias'

import re
import tempfile
import os
import subprocess
import inco.pln.tagging_constants as constants


class TreeTagger(TaggerI):
    """
    Wrapper para NLTK de TreeTagger
    """

    def __init__(self, tagger_path):
        self.tagger_path = tagger_path
        if not os.path.isfile(tagger_path):
            raise Exception("No se encuentra ejecutable de TreeTagger.")

    def tag(self, tokens):
        return self.__tag_custom(tokens, False)

    def tag_full(self, tokens):
        return self.__tag_custom(tokens, True)

    def __tag_custom(self, tokens, is_full):
        result = []
        # tenemos una lista de tokens, tenemos que guardarlo en un archivo.
        string = "\n".join(tokens)

        temp_input = tempfile.NamedTemporaryFile(delete=False, prefix='treetagger_input_')
        temp_output = tempfile.NamedTemporaryFile(delete=False, prefix='treetagger_output_')

        # escribir string a archivo temp de entrada
        temp_input.write(string.encode("utf-8"))

        output_name = temp_output.name
        input_name = temp_input.name

        temp_input.close()
        temp_output.close()

        TreeTagger.__execute(self.tagger_path, input_name, output_name)

        # hay que procesar el archivo leido, hay que leerlo primero.
        with open(output_name) as output_file:
            for line in output_file:
                converted_line = TreeTagger.__convert_line(line)

                if is_full:
                    result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                        (constants.LEMMA, converted_line[constants.LEMMA]),
                                        (constants.COARSE_TAG, converted_line[constants.COARSE_TAG]),
                                        (constants.POS_TAG, converted_line[constants.POS_TAG]),
                                        (constants.FEATURES, dict([
                                            (constants.TAGGER, constants.TAGGERS_TREETAGGER),
                                            (constants.ORIGINAL_TAG, converted_line[constants.ORIGINAL_TAG])
                                        ]))]))
                else:
                    result.append(dict([(constants.WORD, converted_line[constants.WORD]),
                                        (constants.ORIGINAL_TAG, converted_line[constants.ORIGINAL_TAG])]))

        os.remove(input_name)
        os.remove(output_name)

        return result

    @staticmethod
    def __execute(tagger_path, input_file_path, output_file_path):
        """
        Ejecuta TreeTagger sobre un archivo, y escribe la salida en otro.
        """

        # la ejecucion es de la forma INPUT OUTPUT

        bat_name = "tag-spanish.bat"

        # verificar que la ruta del tagger pasada incluya el ejecutable, incluirlo si no esta
        # TODO windows / linux?

        execution_string = tagger_path
        if not execution_string.endswith(bat_name):
            execution_string = os.path.join(tagger_path, bat_name)

        execution_string += " " + input_file_path
        execution_string += " " + output_file_path

        print execution_string

        res_code = subprocess.call(execution_string)
        # validar result code

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
        """
        # forma: palabra, lemma, coarse tag, pos tag, original tag
        tree_tagger_regular_expression = re.compile("^(.*)?\t(.*)?\t(.*)?$")

        utf8line = input_line.decode('utf8')
        parsed_line = tree_tagger_regular_expression.match(utf8line)

        tags = TreeTagger.__translate_tag(parsed_line.group(2), parsed_line.group(1))

        result_object = {constants.WORD: parsed_line.group(1), constants.LEMMA: parsed_line.group(3),
                         constants.ORIGINAL_TAG: parsed_line.group(2),
                         constants.COARSE_TAG: tags[0], constants.POS_TAG: tags[1]}

        return result_object

    @staticmethod
    def __translate_tag(tree_tagger_tag, symbol=None):
        """
        Convierte un tag de TreeTagger a un par (coarse_tag, pos_tag) usando las etiquetas Eagle.
        """

        coarse_tag = None
        pos_tag = None

        if tree_tagger_tag == "ACRNM":
            # acronimo
            coarse_tag = 'n'
            pos_tag = 'NC00000'
        elif tree_tagger_tag == 'ADJ':
            # adjetivo
            coarse_tag = 'a'
            pos_tag = 'A00000'
        elif tree_tagger_tag == 'ADV':
            # adverbio
            coarse_tag = 'r'
            pos_tag = 'R0'
        elif tree_tagger_tag == 'ALFP':
            # plural de una letra del alfabeto (as/aes, bes)
            coarse_tag = 'n'
            pos_tag = 'NCFPV00'
        elif tree_tagger_tag == 'ALFS':
            # singular de una letra del alfabeto
            coarse_tag = 'n'
            pos_tag = 'NCFSV00'
        elif tree_tagger_tag == 'ART':
            # articulo
            coarse_tag = 'd'
            pos_tag = 'DA0000'
        elif tree_tagger_tag == 'BACKSLASH':
            # barra invertida
            coarse_tag = 'f'
            pos_tag = 'Fh'
        elif tree_tagger_tag == 'CARD':
            # cardinales
            coarse_tag = 'f'
            pos_tag = 'Fz'
        elif tree_tagger_tag == 'CC':
            # conjuncion coordinadora (y, o)
            coarse_tag = 'c'
            pos_tag = 'CC'
        elif tree_tagger_tag == 'CCAD':
            # conjuncion coordinadora adversativa
            coarse_tag = 'c'
            pos_tag = 'CC'
        elif tree_tagger_tag == 'CCNEG':
            # conjuncion coordinadora negativa
            coarse_tag = 'c'
            pos_tag = 'CC'
        elif tree_tagger_tag == 'CM':
            # coma
            coarse_tag = 'f'
            pos_tag = 'Fc'
        elif tree_tagger_tag == 'CODE':
            # codigo alfanumerico
            # ################## y esto?
            coarse_tag = 'r'
            pos_tag = 'R0'
        elif tree_tagger_tag == 'COLON':
            # dos puntos (:)
            coarse_tag = 'f'
            pos_tag = 'Fd'
        elif tree_tagger_tag == 'CQUE':
            # que (conjuncion)
            coarse_tag = 'c'
            pos_tag = 'CS'
        elif tree_tagger_tag == 'CSUBF':
            # conjuncion subordinada que introduce clausulas finitas (apenas)
            coarse_tag = 'c'
            pos_tag = 'CS'
        elif tree_tagger_tag == 'CSUBI':
            # conjuncion subordinada que introduce clausulas infinitas (al)
            coarse_tag = 'c'
            pos_tag = 'CS'
        elif tree_tagger_tag == 'CSUBX':
            # conjuncion subordinada no especificada para subtipo (aunque)
            coarse_tag = 'c'
            pos_tag = 'CS'
        elif tree_tagger_tag == 'DASH':
            # guion
            coarse_tag = 'f'
            pos_tag = 'Fg'
        elif tree_tagger_tag == 'DM':
            # pronombres demostrativos
            coarse_tag = 'p'
            pos_tag = 'PD000000'
        elif tree_tagger_tag == 'DOTS':
            # puntos suspensivos (...)
            coarse_tag = 'f'
            pos_tag = 'Fs'
        elif tree_tagger_tag == 'FO':
            # formula
            # ################## y esto?
            coarse_tag = 'r'
            pos_tag = 'R0'
        elif tree_tagger_tag == 'FS':
            # fin de sentencia
            if symbol is not None:
                if symbol == u'¿':
                    pos_tag = "Fia"
                elif symbol == '?':
                    pos_tag = "Fit"

            if pos_tag is None:
                pos_tag = 'Fp'

            coarse_tag = 'f'
        elif tree_tagger_tag == 'INT':
            # pronombres interrogativos
            # aca estamos perdiendo mucha informacion, como si es plural o no
            coarse_tag = 'p'
            pos_tag = 'PT000000'
        elif tree_tagger_tag == 'ITJN':
            # interjeccion (oh, ja)
            coarse_tag = 'i'
            pos_tag = 'I'
        elif tree_tagger_tag == 'LP':
            # parentesis izquierdo
            coarse_tag = 'f'
            pos_tag = 'Fpa'
        elif tree_tagger_tag == 'NC':
            # sustantivos comunes
            coarse_tag = 'n'
            pos_tag = 'NC00000'
        elif tree_tagger_tag == 'NEG':
            # negacion
            coarse_tag = 'r'
            pos_tag = 'RN'
        elif tree_tagger_tag == 'NMEA':
            # sustantivos de medida (litros, metros)
            coarse_tag = 'Z'
            pos_tag = 'Zu'
        elif tree_tagger_tag == 'NMON':
            # nombre de mes
            coarse_tag = 'w'
            pos_tag = 'W'
        elif tree_tagger_tag == 'NP':
            # nombres propios
            coarse_tag = 'n'
            pos_tag = 'NP00000'
        elif tree_tagger_tag == 'ORD':
            # ordinales (primer, primera, primeras)
            # aca tambien estamos perdiendo la forma y plural/singular
            coarse_tag = 'a'
            pos_tag = 'AO0000'
        elif tree_tagger_tag == 'PAL':
            # al
            coarse_tag = 's'
            pos_tag = 'SPCMS'
        elif tree_tagger_tag == 'PDEL':
            # del
            coarse_tag = 's'
            pos_tag = 'SPCMS'
        elif tree_tagger_tag == 'PE':
            # palabra extranjera
            # como taggeamos esto en freeling?
            coarse_tag = 'r'
            pos_tag = 'R0'
        elif tree_tagger_tag == 'PERCT':
            # signo de porcentaje
            coarse_tag = 'f'
            pos_tag = 'Ft'
        elif tree_tagger_tag == 'PNC':
            # palabra sin clasificar
            # como taggeamos esto?
            coarse_tag = 'r'
            pos_tag = 'R0'
        elif tree_tagger_tag == 'PPC':
            # clitico pronombre personal (le, les)
            # aca tambien perdemos la persona y plural/singular.
            coarse_tag = 'p'
            pos_tag = 'PP000000'
        elif tree_tagger_tag == 'PPO':
            # pronombre posesivo (mi, su, sus)
            # aca tambien perdemos la persona y plural/singular.
            coarse_tag = 'p'
            pos_tag = 'PX000000'
        elif tree_tagger_tag == 'PPX':
            # cliticos y pronombres personales (nos, me, nosotros, te)
            # aca tambien perdemos la persona y plural/singular.
            coarse_tag = 'p'
            pos_tag = 'PP000000'
        elif tree_tagger_tag == 'PREP':
            # preposicion
            coarse_tag = 's'
            pos_tag = 'SP000'
        elif tree_tagger_tag == 'PREP/DEL':
            # preposicion compleja (despues del)
            coarse_tag = 's'
            pos_tag = 'SP000'
        elif tree_tagger_tag == 'QT':
            # comillas dobles o simples
            coarse_tag = 'F'
            pos_tag = 'Fe'
        elif tree_tagger_tag == 'QU':
            # cuantificadores (sendas, cada)
            coarse_tag = 'd'
            pos_tag = 'DI0FP'
        elif tree_tagger_tag == 'REL':
            # pronombres relativos (cuyas, cuyo)
            coarse_tag = 'p'
            pos_tag = 'PR000000'
        elif tree_tagger_tag == 'RP':
            # parentesis derecho
            coarse_tag = 'F'
            pos_tag = 'Fpa'
        elif tree_tagger_tag == 'SE':
            # se (como particula)
            coarse_tag = 'p'
            pos_tag = 'PP3CN000'
        elif tree_tagger_tag == 'SEMICOLON':
            # punto y coma ;
            coarse_tag = 'f'
            pos_tag = 'Fx'
        elif tree_tagger_tag == 'SLASH':
            # /
            coarse_tag = 'f'
            pos_tag = 'Fh'
        elif tree_tagger_tag == 'SYM':
            # simbolos
            # #######y esto?
            coarse_tag = 'a'
            pos_tag = 'A00000'
        elif tree_tagger_tag == 'UMMX':
            # unidad de medida (MHz, km)
            coarse_tag = 'z'
            pos_tag = 'Zu'
        elif tree_tagger_tag == 'VCLIger':
            # clitico gerundio verbo
            coarse_tag = 'v'
            pos_tag = 'V0G0000'
        elif tree_tagger_tag == 'VCLIinf':
            # clitico infinitivo verbo
            coarse_tag = 'v'
            pos_tag = 'V0N0000'
        elif tree_tagger_tag == 'VCLIfin':
            # clitico finito verbo
            coarse_tag = 'v'
            pos_tag = 'V000000'
        elif tree_tagger_tag == 'VEadj':
            # verbo estar. Participio pasado
            coarse_tag = 'v'
            pos_tag = 'V0PS000'
        elif tree_tagger_tag == 'VEfin':
            # verbo estar. Finito
            coarse_tag = 'v'
            pos_tag = 'V000000'
        elif tree_tagger_tag == 'VEger':
            # verbo estar. Gerundio
            coarse_tag = 'v'
            pos_tag = 'V0G0000'
        elif tree_tagger_tag == 'VEinf':
            # verbo estar. Infinitivo
            coarse_tag = 'v'
            pos_tag = 'V0N0000'
        elif tree_tagger_tag == 'VHadj':
            # verbo haber. Participio pasado
            coarse_tag = 'v'
            pos_tag = 'V0PS000'
        elif tree_tagger_tag == 'VHfin':
            # verbo haber. Finito
            coarse_tag = 'v'
            pos_tag = 'V000000'
        elif tree_tagger_tag == 'VHger':
            # verbo haber. Gerundio
            coarse_tag = 'v'
            pos_tag = 'V0G0000'
        elif tree_tagger_tag == 'VHinf':
            # verbo haber. Infinitivo
            coarse_tag = 'v'
            pos_tag = 'V0N0000'
        elif tree_tagger_tag == 'VLadj':
            # verbo lexico. Participio pasado
            coarse_tag = 'v'
            pos_tag = 'V0PS000'
        elif tree_tagger_tag == 'VLfin':
            # verbo lexico. Finito
            coarse_tag = 'v'
            pos_tag = 'V000000'
        elif tree_tagger_tag == 'VLger':
            # verbo lexico. Gerundio
            coarse_tag = 'v'
            pos_tag = 'V0G0000'
        elif tree_tagger_tag == 'VLinf':
            # verbo lexico. Infinitivo
            coarse_tag = 'v'
            pos_tag = 'V0N0000'
        elif tree_tagger_tag == 'VMadj':
            # verbo modal. Participio pasado
            coarse_tag = 'v'
            pos_tag = 'V0PS000'
        elif tree_tagger_tag == 'VMfin':
            # verbo modal. Finito
            coarse_tag = 'v'
            pos_tag = 'V000000'
        elif tree_tagger_tag == 'VMger':
            # verbo modal. Gerundio
            coarse_tag = 'v'
            pos_tag = 'V0G0000'
        elif tree_tagger_tag == 'VMinf':
            # verbo modal. Infinitivo
            coarse_tag = 'v'
            pos_tag = 'V0N0000'
        elif tree_tagger_tag == 'VSadj':
            # verbo ser. Participio pasado
            coarse_tag = 'v'
            pos_tag = 'V0PS000'
        elif tree_tagger_tag == 'VSfin':
            # verbo ser. Finito
            coarse_tag = 'v'
            pos_tag = 'V000000'
        elif tree_tagger_tag == 'VSger':
            # verbo ser. Gerundio
            coarse_tag = 'v'
            pos_tag = 'V0G0000'
        elif tree_tagger_tag == 'VSinf':
            # verbo ser. Infinitivo
            coarse_tag = 'v'
            pos_tag = 'V0N0000'

        return coarse_tag, pos_tag


# nltk.tag.inco.TreeTagger = TreeTagger

