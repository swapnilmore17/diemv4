from treelib import Tree, Node


class TreeUtility:
    def __init__(self):
        self.tree = Tree()

    def add(self, node, parent_id):
        if parent_id is None:
            node = self.tree.create_node(data=node)
        else:
            node = self.tree.create_node(parent=parent_id, data=node)
        return node.identifier

    def get_node(self, node_id):
        return self.tree.get_node(node_id)

    def prune(self, node_id):
        tree = self.tree.remove_subtree(node_id)
        return tree

    def commit(self, node_id):
        parent = self.tree.parent(node_id)
        if parent is not None:
            siblings_list = self.tree.children(parent.identifier)
            for node in siblings_list:
                if node.identifier == node_id:
                    pass
                else:
                    self.tree.remove_node(node.identifier)
        return self.tree
