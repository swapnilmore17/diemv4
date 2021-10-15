#module keeps track of a tree of all blocks pending
#commitment and the votes they receive.
from ledger import Ledger as ledger

class VoteInfo:
    def __init__(self,id,round,parent_id,parent_round,exec_state_id):
        self.id = id
        self.round=round
        self.parent_id =parent_id
        self.parent_round=parent_round
        self.exec_state_id = exec_state_id
        
class LedgerCommitInfo:
    def __init__(self,commit_state_id,vote_info_hash):
        self.commit_state_id = commit_state_id
        self.vote_info_hash = vote_info_hash

class VoteMsg:
    def __init__(self,vote_info,ledger_commit_info,high_commit_qc,sender,signature):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender=sender
        self.signature=signature

class QC:
    def __init__(self,vote_info,ledger_commit_info,signatures,author,author_signature) -> None:
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = author
        self.author_signature = author_signature

class Block:

    def __init__(self,author,round,payload,qc,id) -> None:
        self.author=author
        self.round=round
        self.payload=payload
        self.qc = new QC(qc)
        self.id = id

class BlockTree:
    def __init__(self,pending_block_tree,pending_votes,high_qc,high_commit_qc) -> None:
        
        #tree object
        
        self.pending_block_tree = pending_block_tree
        
        self.pending_votes=pending_votes
        self.high_qc=high_qc
        self.high_commit_qc=high_commit_qc
    
    def process_qc(self,qc):
        if qc.ledger_commit_info:
            ledger.commit(qc.vote_info.parent_id)
            pending_block_tree.prune(qc.vote_info.parent_id)
            self.high_commit_qc = max(qc,self.high_commit_qc)
        self.high_qc = max(qc,self.high_qc)
    
    def execute_and_insert(b):
        ledger.speculate(b.qc.block_id,b.id,b.payload)
        pending_block_tree.add(b)

    

    