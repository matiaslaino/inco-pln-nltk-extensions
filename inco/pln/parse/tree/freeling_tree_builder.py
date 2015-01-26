import re

__author__ = 'Matias'

from nltk.tree import Tree


class FreeLingTreeBuilder():
    def __init__(self):
        pass

    __regex_leaf = ".*\((.*?)-\)$"
    __regex_inner_node = "\+?(.*)\[$"
    __regex_line = "( *)(.*)"

    def build(self, tree_str):
        lines = tree_str.split('\n')

        c_regex_line = re.compile(self.__regex_line)
        c_regex_inner_node = re.compile(self.__regex_inner_node)
        c_regex_leaf = re.compile(self.__regex_leaf)

        stack = []

        for line in lines:
            line = line.rstrip()
            if line != "" and not line.isspace():
                line_match = c_regex_line.match(line)

                content = line_match.group(2)

                if content.startswith(u"]"):
                    last_pop = stack.pop()
                else:
                    inner_node_match = c_regex_inner_node.match(content)
                    leaf_match = c_regex_leaf.match(content)
                    if inner_node_match is not None:
                        # armar un nodo interno
                        tree_node = Tree(inner_node_match.group(1), [])
                        is_inner = True
                    else:
                        # hoja
                        tree_node = Tree(leaf_match.group(1), [])
                        is_inner = False

                    if len(stack) > 0 and stack[-1] is not None:
                        stack[-1].append(tree_node)

                    if is_inner:
                        stack.append(tree_node)

        return last_pop