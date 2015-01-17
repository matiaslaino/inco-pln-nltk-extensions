# coding=utf-8
__author__ = 'Matias'

from nltk import Tree


class DotLanguageConverter:
    """
    Conversor de nltk.tree.Tree a string en lenguaje DOT.
    """

    def __init__(self):
        pass

    def convert(self, tree):
        """
        :type tree: nltk.tree.Tree
        :param tree El árbol a convertir.
        :rtype: str
        :return: El árbol, serializado a string en lenguaje DOT.
        """

        dot_string = "digraph parse_tree {\n"

        for child in tree:
            dot_string += self.__convert(child, tree)

        dot_string += "}"

        return dot_string

    def __convert(self, node, parent):
        string = "\t"

        node_value = node.label() if type(node) is Tree else node

        string += parent.label() + " -> " + node_value + ";\n"

        if type(node) is Tree:
            for child in node:
                string += self.__convert(child, node)

        return string