#module keeps track of a tree of all blocks pending
#commitment and the votes they receive.
from ledger import Ledger as Ledger
from treeutility import TreeUtility
import uuid

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
    def __init__(self,vote_info,ledger_commit_info,high_commit_qc,sender):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.high_commit_qc = high_commit_qc
        self.sender=sender
        self.signature=hash(ledger_commit_info)

class QC:
    def __init__(self,vote_info,ledger_commit_info,signatures,author):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = author
        #####
        #####
        ####
        self.author_signature = hash(author)

#checked with function call
class Block:
    def __init__(self,author,round,payload,qc,id):
        self.author=author
        self.round=round
        self.payload=payload
        self.qc = qc
        self.id = id

class BlockTree:


    ####### initialized in master.da
    def __init__(self):
        
        self.pending_block_tree = TreeUtility()
        
        self.pending_votes={}
        self.high_qc=None
        self.high_commit_qc=None
    
    def process_qc(self,qc):
        if qc.ledger_commit_info:
            Ledger.commit(qc.vote_info.parent_id)
            self.pending_block_tree=self.pending_block_tree.prune(qc.vote_info.parent_id)
            self.high_commit_qc = max(qc,self.high_commit_qc)
            ######compare qc.round in the line above
        self.high_qc = max(qc,self.high_qc)
    
    def execute_and_insert(self,b):
        Ledger.speculate(b.qc.vote_info.id,b.id,b)
        #how to get parent id
        #
        #
        ##
        #
        self.pending_block_tree=self.pending_block_tree.add(b)
    
    def generate_block(self,txns,current_round,author):
        #where will author come from
        b = Block(author,current_round,txns,self.high_qc,uuid.uuid4())
        return b

    ############
    #
    def process_vote(self,v,f):
        self.process_qc(v.high_commit_qc)
        vote_idx = hash(v.ledger_commit_info)
        #if vote idx does not exist???
        self.pending_votes[vote_idx] = self.pending_votes[vote_idx] + v.signature
        if len(self.pending_votes[vote_idx]) == 2*f+1:
            commit_info = hash(v.state_id)
            votes = self.pending_votes[vote_idx]

            #
            #where will author come from
            #
            return QC(v.vote_info,commit_info,votes,author)
        return None

    

    