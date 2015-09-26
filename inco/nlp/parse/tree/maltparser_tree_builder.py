import re

"""
This module contains the classes required to convert the output of MaltParser into a more
usable form, such as a NLTK's Tree.
"""

# TODO: put MaltParser sample output here.


__author__ = 'Matias Laino'

from nltk.tree import Tree


class MaltParserTreeBuilder():
    def __init__(self):
        pass

    # regular expression to recognize a MaltParser output line, and its components
    __regex_line = "(\d+)\s+(.+)\s+.+\s+\w+\s+\w+\s+_\s+(\d+)\s+\w+\s+_\s+_"

    def build(self, tree_str):
        """
        Builds a tree from the output of MaltParser.

        @param tree_str: the string representation of the output intended for parsing.
        @type tree_str: str
        @return: the parse tree
        @rtype: Tree
        """

        lines = tree_str.split('\n')

        c_regex_line = re.compile(self.__regex_line, re.UNICODE)

        # TODO: put this as a parameter
        # dependency dictionary. The key is a node, the values are its dependencies.
        self.dependencies = {}
        self.words = [(0, "ROOT")]

        for line in lines:
            if line != "":
                line_match = c_regex_line.match(line)

                # node number
                num = int(line_match.group(1))

                word = line_match.group(2)
                dependency = int(line_match.group(3))

                if dependency not in self.dependencies:
                    self.dependencies[dependency] = []

                item = (num, word)

                self.words.append(item)
                self.dependencies[dependency].append(item)

        root = self.__build_tree(0)

        return root

    def __build_tree(self, node_num):
        word_tuple = self.words[node_num]
        tree_node = Tree(word_tuple[1], [])

        node_dependencies = self.dependencies.get(node_num)
        if node_dependencies is not None:
            for dependency in node_dependencies:
                dependency_node = self.__build_tree(dependency[0])
                tree_node.append(dependency_node)

        return tree_node
