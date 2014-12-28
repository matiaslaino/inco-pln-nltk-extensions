# coding=utf-8
import json

import nltk

from inco.pln.parse.maltparser import MaltParser


__author__ = 'Matias'

# import os
#
# string = "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin\\analyzer.exe"
# string2 = "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin"
# string3 = "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin\\"
# print os.path.basename(string)
# print os.path.abspath(string)
# print os.path.dirname(string)
# print os.path.dirname(string2)
# print os.path.dirname(string3)

import inco.pln.tag.treetagger
import inco.pln.tag.freeling
import inco.pln.parse.freeling

tagger_tt = inco.pln.tag.treetagger.TreeTagger(
    "C:\\Users\\Matias\\Downloads\\tree-tagger-windows-3.2\\TreeTagger\\bin\\tag-spanish.bat")
tagger_fl = inco.pln.tag.freeling.FreeLing(
    "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin\\analyzer.exe")

tokens = [u"En", u"el", u"tramo", u"de", u"Telefónica", u"un", u"toro", u"descolgado", u"ha", u"creado", u"peligro",
          u"tras", u"embestir", u"contra", u"un", u"grupo", u"de", u"mozos", u"."]
# tagged = tt.tag(tokens)
# print tagged
full = tagger_fl.tag_full(tokens)
# print full



#
# obj = dict(word="algo",
# lemma="algo",
#      coarse_tag="algo",
#      pos_tag="algo",
#      features=dict(
#          tagger='TreeTagger',
#          original_tag="algo"
#      ))
# #
string = json.dumps(full)
#
# print string
#
# obj2 = json.loads(string)
#
# print obj2[0]

parser_mp = MaltParser("C:\\Users\\Matias\\Downloads\\maltparser-1.8\\maltparser-1.8\\maltparser-1.8.jar",
                       "C:\\Users\\Matias\\Downloads\\maltparser-1.8\\maltparser-1.8\\ModeloESP\\espmalt-1.0.mco")
parser_fl = inco.pln.parse.freeling.FreeLing(
    "C:\\Users\\Matias\\Downloads\\freeling-3.1-win\\freeling-3.1-win\\bin\\analyzer.exe")


# print "--------- PARSE MALTPARSER ----------"
# print parser_mp.parse(string)
# print "--------- PARSE FREELING ----------"
# print parser_fl.parse(string)

# from nltk import CFG
#
groucho_grammar = nltk.grammar.parse_cfg("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")

parser = nltk.parse.ChartParser(groucho_grammar)
parsed = parser.parse(["I", "shot", "an", "elephant", "in", "my", "pajamas"])

print parsed

import nltk.parse.malt

nltk.parse.malt.MaltParser