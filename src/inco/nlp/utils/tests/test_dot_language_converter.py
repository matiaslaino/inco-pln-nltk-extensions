from inco.nlp.utils.dot_language_converter import DotLanguageConverter

__author__ = 'Matias Laino'

import unittest
from nltk import Tree


class TestConversionFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def testConvert(self):
        sample_tree = Tree.fromstring("(S (NP I) (VP (V saw) (NP him)))")
        converter = DotLanguageConverter()
        str = converter.convert(sample_tree)

        expected_tree_string = ("digraph parse_tree {\n"
                                "\t\"S\" [label=\"S\"];\n"
                                "\t\"NP\" [label=\"NP\"];\n"
                                "\t\"S\"-> \"NP\";\n"
                                "\t\"I\" [label=\"I\"];\n"
                                "\t\"NP\"-> \"I\";\n"
                                "\t\"VP\" [label=\"VP\"];\n"
                                "\t\"S\"-> \"VP\";\n"
                                "\t\"V\" [label=\"V\"];\n"
                                "\t\"VP\"-> \"V\";\n"
                                "\t\"saw\" [label=\"saw\"];\n"
                                "\t\"V\"-> \"saw\";\n"
                                "\t\"NP_1\" [label=\"NP\"];\n"
                                "\t\"VP\"-> \"NP_1\";\n"
                                "\t\"him\" [label=\"him\"];\n"
                                "\t\"NP_1\"-> \"him\";\n"
                                "}")


        self.assertEqual(str, expected_tree_string)

if __name__ == '__main__':
    unittest.main()