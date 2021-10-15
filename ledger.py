class Ledger:
    def speculate(prev_block_id,block_id,txns):
        #apply txns speculatively
        # speculatively executes a block of transactions over the previous block state and returns a new ledger state id

    def pending_state(block_id):
        #find the pending state for the given block id or ⊥ if not present

    def commit(block_id):
        #commit the pending prefix of the given block id and prune other branches
        #exports to the persistent ledger store a committed branch. 
        # it discards speculated branches that fork from ancestors of the committed state.

    def commited_block(block_id):
        #return commited block with id=block_id