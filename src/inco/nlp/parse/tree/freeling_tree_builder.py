import re

"""
This module contains the classes required to convert the output of the FreeLing parser into a more
usable form, such as a NLTK's Tree.
"""

# TODO: put FreeLing sample output here.

__author__ = 'Matias Laino'

from nltk.tree import Tree


class FreeLingTreeBuilder():
    """
    Class for building nltk.tree.Tree from the output of the FreeLing parser.
    """

    def __init__(self):
        pass

    # Regular expression to recognize leaves.
    __regex_leaf = ".*\((.*?)-\)$"
    # Regular expression to regognize inner nodes.
    __regex_inner_node = "\+?(.*)\[$"
    # General reular expression to clear leading spaces. TODO: may be accomplished with native python operations
    __regex_line = "( *)(.*)"

    def build(self, tree_str):
        """
        Builds a tree from the output of the FreeLing parser.

        @param tree_str: the string representation of the output intended for parsing.
        @type tree_str: str
        @return: the parse tree
        @rtype: Tree
        """

        lines = tree_str.split('\n')

        c_regex_line = re.compile(self.__regex_line)
        c_regex_inner_node = re.compile(self.__regex_inner_node)
        c_regex_leaf = re.compile(self.__regex_leaf)

        # in this stack we'll put intermediate nodes as we move deeper into the parse tree.
        # This is a depth-first algorithm.
        stack = []

        last_pop = None

        for line in lines:
            line = line.rstrip()
            if line != "" and not line.isspace():
                line_match = c_regex_line.match(line)

                content = line_match.group(2)

                if content.startswith(u"]"):
                    # the previous line was the last child of the last item on the
                    # stack, pop!
                    last_pop = stack.pop()
                else:
                    inner_node_match = c_regex_inner_node.match(content)
                    leaf_match = c_regex_leaf.match(content)
                    if inner_node_match is not None:
                        # build inner node
                        tree_node = Tree(inner_node_match.group(1), [])
                        is_inner = True
                    else:
                        # build leave
                        node_content = leaf_match.group(1)
                        node_content = node_content.rstrip(' ').lstrip(' ').replace(' ', '_')
                        tree_node = Tree(node_content, [])
                        is_inner = False

                    # this is a child of the last item on the stack, if any.
                    if len(stack) > 0 and stack[-1] is not None:
                        stack[-1].append(tree_node)

                    # if this is an inner node, it means next string coming up is a child of this one,
                    # save into stack.
                    if is_inner:
                        stack.append(tree_node)

        return last_pop