from treelib import Tree, Node
import pickle
from treeutility import TreeUtility
class Ledger:
    def __init__(self):
        self.ledger_state = None # ledger_state/commit_id in memory
        self.blockid_to_nodeid_mapper = {} # mapping of Block ID to Node ID
        self.blockid_to_commitid_mapper = {} # mapping of Block ID to commit_id
        self.tree_utility = TreeUtility() # Tree utility to store pending block tree

    # Adds txns as payload to the node in the pending tree and maintains mapping
    def speculate(self, prev_block_id, block_id, txns):
        parent_id = None
        if prev_block_id is not None:
            parent_id = self.blockid_to_nodeid_mapper[prev_block_id] #fetch parent ID if it exists
        if parent_id is None:
            node_id = self.tree_utility.add(txns, None) #add node to tree with payload=txns
            self.blockid_to_nodeid_mapper[block_id] = node_id # store mapping
        else:
            node_id = self.tree_utility.add(txns, parent_id)
            self.blockid_to_nodeid_mapper[block_id] = node_id
        return block_id 

    # Returns Ledger State/ Commit ID based on Block ID
    def pending_state(self, block_id):
        return self.blockid_to_commitid_mapper[block_id]

    # Commits block to persistent ledger and returns ledger state/ commit ID
    def commit(self, block_id):
        node_id = self.blockid_to_nodeid_mapper[block_id]
        if node_id is not None: 
            node = self.tree_utility.get_node(node_id)
            filename = "ledgerstore"
            ledgerfile = open(filename, "ab")
            # Generate hash of previous state with committed block's payload
            self.ledger_state = hash(str(self.ledger_state) + str(node.data))
            self.blockid_to_commitid_mapper[block_id] = str(self.ledger_state)
            pickle.dump(self.ledger_state, ledgerfile) # Store ledger state into ledger
            pickle.dump(node.data, ledgerfile) # Store payload into ledger
            self.tree_utility.commit(node_id) #Remove uncommitted sibling branches
            return str(self.ledger_state)       

    # Returns block from pending tree using block ID
    def commited_block(self, block_id):
        node_id = self.blockid_to_nodeid_mapper[block_id]
        if node_id is not None:
            node = self.tree_utility.get_node(node_id)
            return node.data    