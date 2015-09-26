# coding=utf-8
__author__ = 'Matias Laino'

from nltk import Tree


class DotLanguageConverter:
    """
    Converter from an NLTK Tree to DOT Language.
    """

    def __init__(self):
        self.node_names = {}
        pass

    def convert(self, tree):
        """
        @type tree: nltk.tree.Tree
        @param tree: tree to convert to DOT.
        @rtype: str
        @return: the tree, serialized to string in DOT language.
        """

        dot_string = "digraph parse_tree {\n"

        tree_name_label_pair = self.__make_node_name_and_label(tree)
        dot_string += "\t\"" + tree_name_label_pair[0] + "\" [label=\"" + tree_name_label_pair[1] + "\"];\n"

        for child in tree:
            dot_string += self.__convert(child, tree_name_label_pair[0])

        dot_string += "}"

        return dot_string

    def __convert(self, node, parent_name):
        """
        Converts a node to DOT, working recursively on its children, if any.

        @param node: node to be converted
        @param parent: parent of the node, this is never None.
        @return: the node, in a DOT language string.
        """

        tree_name_label_pair = self.__make_node_name_and_label(node)
        string = "\t\"" + tree_name_label_pair[0] + "\" [label=\"" + tree_name_label_pair[1] + "\"];\n"

        string += "\t\"" + parent_name + "\"-> \"" + tree_name_label_pair[0] + "\";\n"

        if type(node) is Tree:
            for child in node:
                string += self.__convert(child, tree_name_label_pair[0])

        return string

    def __make_node_name_and_label(self, node):
        """

        @param node:
        @return:
        """
        if type(node) is Tree:
            node_name = node.label()
            node_label = node.label()
        else:
            node_name = node
            node_label = node

        if node_name in self.node_names:
            self.node_names[node_name] += 1
            node_name += "_" + str(self.node_names[node_name] - 1)
        else:
            self.node_names[node_name] = 1

        return node_name, node_label