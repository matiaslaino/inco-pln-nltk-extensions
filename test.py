# # coding=utf-8
# import json
#
# from inco.pln.parse.maltparser import MaltParser
#
# __author__ = 'Matias'
#
# import inco.pln.tag.convert
# import inco.pln.tag.freeling
# import inco.pln.parse.freeling
# import inco.pln.tokenize.freeling
#
# tagger_tt = inco.pln.tag.convert.TreeTagger(
# "C:\\Users\\Matias\\Downloads\\tree-tagger-windows-3.2\\TreeTagger\\bin\\tag-spanish.bat")
# tagger_fl = inco.pln.tag.freeling.FreeLing(
#     "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin\\analyzer.exe", True)
# tokenizer = inco.pln.tokenize.freeling.FreeLing(
#     "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin\\analyzer.exe", True)
#
# string = u"En el tramo de Telefónica, un toro descolgado ha creado peligro tras embestir contra un grupo de mozos."
# tokens = tokenizer.tokenize(string)
#
# # tokens = [u"En", u"el", u"tramo", u"de", u"Telefónica", u"un", u"toro", u"descolgado", u"ha", u"creado", u"peligro",
# # u"tras", u"embestir", u"contra", u"un", u"grupo", u"de", u"mozos", u"."]
#
# tagged_tokens_fl = tagger_fl.tag(tokens)
#
# # fl_full = tagger_fl.tag_full(tokens)
# # tt_full = tagger_tt.tag_full(tokens)
#
# # string_fl = json.dumps(fl_full)
# # string_tt = json.dumps(tt_full)
#
#
#
# # parser_mp = MaltParser("C:\\Users\\Matias\\Downloads\\maltparser-1.8\\maltparser-1.8\\maltparser-1.8.jar",
# #                        "C:\\Users\\Matias\\Downloads\\maltparser-1.8\\maltparser-1.8\\ModeloESP\\espmalt-1.0.mco")
# parser_fl = inco.pln.parse.freeling.FreeLing(
#     "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin\\analyzer.exe")
#
# # print "--------- PARSE MALTPARSER (FREELING TAGGER) ----------"
# # print parser_mp.parse(string_fl, True).draw()
# print "--------- PARSE FREELING (FREELING TAGGER) ----------"
# print parser_fl.tagged_parse(tagged_tokens_fl).draw()
#
# # print "--------- PARSE MALTPARSER (TREETAGGER TAGGER) ----------"
# # print parser_mp.parse(string_tt, True).draw()
# # print "--------- PARSE FREELING (TREETAGGER TAGGER) ----------"
# # print parser_fl.parse(string_tt, True).draw()

# from nltk.parse.malt import MaltParser
#
# real_mp = MaltParser(mco="espmalt-1.0.mco",
#                      working_dir=r"C:\\Users\\Matias\\Downloads\\maltparser-1.8\\maltparser-1.8\\")
# real_mp.config_malt(bin='C:\\Users\\Matias\\Downloads\\maltparser-1.8\\maltparser-1.8\\')
# parsed = real_mp.raw_parse("Hola, que tal?")
#
# print parsed



from inco.pln.tokenize.freeling import FreeLing
from inco.pln.tag.treetagger import TreeTagger
from inco.pln.parse.stanford.stanford_shift_reduce import StanfordShiftReduceParser

texto = "Esto es un texto de prueba, sin tokenizar"

ruta_a_treetagger = "D:/Matias/Proyecto-PLN/tree-tagger-windows-3.2/TreeTagger/bin/tag-spanish.bat"
ruta_a_freeling = "D:/Matias/Proyecto-PLN/freeling-3.1-win/freeling-3.1-win/bin/analyzer.exe"
ruta_a_stanford_sr = "D:/Matias/Proyecto-PLN/stanford/stanford-parser.jar"
ruta_a_modelo_stanford_sr = "D:/Matias/Proyecto-PLN/stanford/stanford-srparser-2014-10-23-models.jar"

freeling_tokenizer = FreeLing(ruta_a_freeling)
tagger = TreeTagger(ruta_a_treetagger, freeling_tokenizer)
parser = StanfordShiftReduceParser(ruta_a_stanford_sr, ruta_a_modelo_stanford_sr, tagger)

print parser.parse(texto)