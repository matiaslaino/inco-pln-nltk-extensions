from inco.pln.utils.dot_language_converter import DotLanguageConverter

__author__ = 'Matias'

import random
import unittest
from nltk import Tree
from inco.pln.utils import dot_language_converter

class TestConversionFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def testConvert(self):
        sample_tree = Tree.fromstring("(S (NP I) (VP (V saw) (NP him)))")
        converter = DotLanguageConverter()
        str = converter.convert(sample_tree)

        expected_tree_string = ("digraph parse_tree {\n"
                         "\tS -> NP;\n"
                         "\tNP -> I;\n"
                         "\tS -> VP;\n"
                         "\tVP -> V;\n"
                         "\tV -> saw;\n"
                         "\tVP -> NP;\n"
                         "\tNP -> him;\n"
                         "}"
        )

        self.assertEqual(str, expected_tree_string)

if __name__ == '__main__':
    unittest.main()