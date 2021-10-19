from treelib import Tree, Node
import pickle
from treeutility import TreeUtility


class Ledger:
    def __init__(self):
        # print('ledger')
        self.ledger_state = None  # ledger_state/commit_id in memory
        self.blockid_to_nodeid_mapper = {}  # mapping of Block ID to Node ID
        self.blockid_to_commitid_mapper = {}  # mapping of Block ID to commit_id
        self.tree_utility = TreeUtility()  # Tree utility to store pending block tree

    # Adds txns as payload to the node in the pending tree and maintains
    # mapping
    def speculate(self, prev_block_id, block_id, txns):
        # print('4')
        parent_id = None
        if prev_block_id is not None:
            # fetch parent ID if it exists
            parent_id = self.blockid_to_nodeid_mapper[prev_block_id]
        if parent_id is None:
            # add node to tree with payload=txns
            node_id = self.tree_utility.add(txns, None)
            self.blockid_to_nodeid_mapper[block_id] = node_id  # store mapping
        else:
            node_id = self.tree_utility.add(txns, parent_id)
            self.blockid_to_nodeid_mapper[block_id] = node_id

        output('Added new block')
        return block_id

    # Returns Ledger State/ Commit ID based on Block ID
    def pending_state(self, block_id):
        # print('1')

        return self.blockid_to_commitid_mapper[block_id]

    # Commits block to persistent ledger and returns ledger state/ commit ID
    def commit(self, block_id):
        node_id = self.blockid_to_nodeid_mapper[block_id]
        # print('2')
        if node_id is not None:
            node = self.tree_utility.get_node(node_id)
            filename = "ledgerstore"
            ledgerfile = open(filename, "ab")
            # Generate hash of previous state with committed block's payload
            self.ledger_state = str(self.ledger_state) + " " + str(node.data)
            self.blockid_to_commitid_mapper[block_id] = str(self.ledger_state)
            # Store ledger state into ledger
            pickle.dump(self.ledger_state, ledgerfile)
            pickle.dump(node.data, ledgerfile)  # Store payload into ledger
            # Remove uncommitted sibling branches
            self.tree_utility.commit(node_id)
            output('Commited block')
            return str(self.ledger_state)
        return ''

    # Returns block from pending tree using block ID
    def commited_block(self, block_id):
        # print('3')
        node_id = self.blockid_to_nodeid_mapper[block_id]
        if node_id is not None:
            node = self.tree_utility.get_node(node_id)
            return node.data
