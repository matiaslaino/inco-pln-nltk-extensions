import re

__author__ = 'Matias'

from nltk.tree import Tree

class MaltParserTreeBuilder():

    # 1 En en s SPS00 _ 10 MOD _ _
    __regex_line = "(\d+)\s+(.+)\s+.+\s+\w+\s+\w+\s+_\s+(\d+)\s+\w+\s+_\s+_"

    def build(self, tree_str):
        lines = tree_str.split('\n')

        c_regex_line = re.compile(self.__regex_line, re.UNICODE)

        self.dependencies = {}
        self.words = [(0, "ROOT")]

        for line in lines:
            if line != "":
                line_match = c_regex_line.match(line)

                num = int(line_match.group(1))
                word = line_match.group(2)
                dependency = int(line_match.group(3))

                if dependency not in self.dependencies:
                    self.dependencies[dependency] = []

                item = (num, word)

                self.words.append(item)
                self.dependencies[dependency].append(item)

        root = self.build_tree(0)

        return root

    def build_tree(self, node_num):
        word_tuple = self.words[node_num]
        tree_node = Tree(word_tuple[1], [])

        node_dependencies = self.dependencies.get(node_num)
        if node_dependencies is not None:
            for dependency in node_dependencies:
                dependency_node = self.build_tree(dependency[0])
                tree_node.append(dependency_node)

        return tree_node
