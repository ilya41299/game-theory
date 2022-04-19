import numpy
from treelib import Tree
import random
import graphviz
from graphviz import Source

DEPTH = 5
num = 0
format = 'pdf'


def create_subtree(current_depth, i):
    tree = Tree()
    parent = i
    if (current_depth % 2):
        tree.create_node("B : " + str(i), parent)
    else:
        tree.create_node("A : " + str(i), parent)

    if (current_depth == DEPTH):
        random_data = [(random.randint(-10, 10), random.randint(-10, 10)) for i in range(3)]
        tree.create_node(random_data[0], 3 * i + 1, parent, data=[random_data[0]])
        tree.create_node(random_data[1], 3 * i + 2, parent, data=[random_data[1]])
        tree.create_node(random_data[2], 3 * i + 3, parent, data=[random_data[2]])
        return tree

    tree.paste(parent, create_subtree(current_depth + 1, i * 3 + 1))
    tree.paste(parent, create_subtree(current_depth + 1, i * 3 + 2))
    tree.paste(parent, create_subtree(current_depth + 1, i * 3 + 3))

    return tree


def find_path(tree: Tree):
    current_depth = tree.depth() - 1
    copy_tree = Tree(tree)

    slice_tree = list(filter(lambda x: tree.level(x.identifier) == current_depth, tree.all_nodes()))
    while (current_depth != -1):
        if (current_depth % 2):
            gamer = 1  # B
        else:
            gamer = 0  # A

        for v in slice_tree:
            children = tree.children(v.identifier)

            max_win = numpy.max(
                [numpy.max([child.data[0][gamer] for i in range(len(child.data[0]))]) for child in children])

            for child in children:
                if child.data[0][gamer] < max_win:
                    tree.remove_subtree(child.identifier)
                else:
                    copy_tree.get_node(v.identifier).tag += f"\n{str([child.data[0]])}"
            v.data = [child.data[0] for child in tree.children(v.identifier)]

        current_depth -= 1
        slice_tree = list(filter(lambda x: tree.level(x.identifier) == current_depth, tree.all_nodes()))
    tree.show()
    copy_tree.to_graphviz("result_tree.gv")
    Source.from_file("result_tree.gv").render(cleanup=True, format=format, view=True)
    return tree


def create_tree():
    tree = Tree()
    count = 0
    tree.create_node("A : 0", 0)
    tree.paste(0, create_subtree(count + 1, 1))
    tree.paste(0, create_subtree(count + 1, 2))
    tree.paste(0, create_subtree(count + 1, 3))

    return tree


if __name__ == '__main__':
    # tree = Tree()
    my_tree = create_tree()
    my_tree.show(key=False, idhidden=False)
    my_tree.to_graphviz("init_tree.gv")
    Source.from_file("init_tree.gv").render(cleanup=True, format=format, view=True)

    find_path(my_tree)
    filename = "truncated_tree.gv"
    my_tree.to_graphviz(filename)
    Source.from_file("truncated_tree.gv").render(cleanup=True, format=format, view=True)
