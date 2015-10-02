import os
from inco.nlp.parse.maltparser import MaltParser
from inco.nlp.parse.stanford.stanford_shift_reduce import StanfordShiftReduceParser

from inco.nlp.tag.freeling import FreeLing as FreeLingTagger
from inco.nlp.tag.treetagger import TreeTagger
from inco.nlp.tokenize.freeling import FreeLing as FreeLingTokenizer
from inco.nlp.parse.freeling import FreeLing as FreeLingParser

text = u"Esto es un texto de prueba, sin tokenizar"

path_treetagger = os.environ['NLP_TREETAGGER']
path_freeling = os.environ['NLP_FREELING']
path_stanford_sr = os.environ['NLP_STANFORDSR']
path_stanford_sr_model = os.environ['NLP_STANFORDSR_MODEL']
path_maltparser = os.environ['NLP_MALTPARSER']
path_maltparser_model = os.environ['NLP_MALTPARSER_MODEL']

freeling_tagger = FreeLingTagger(path_freeling)
freeling_tokenizer = FreeLingTokenizer(path_freeling)
freeling_parser = FreeLingParser(path_freeling)

tagger = TreeTagger(path_treetagger, freeling_tokenizer)
stanford_sr_parser = StanfordShiftReduceParser(path_stanford_sr, path_stanford_sr_model, tagger)
maltparser = MaltParser(path_maltparser, path_maltparser_model, tagger)

tokens = freeling_tokenizer.tokenize(text)

print(next(stanford_sr_parser.parse(tokens)))
print(next(freeling_parser.parse(tokens)))
print(next(maltparser.parse(tokens)))
