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
        self.signature=str(ledger_commit_info.commit_state_id) + str(ledger_commit_info.vote_info_hash)

class QC:
    def __init__(self,vote_info,ledger_commit_info,signatures,author):
        self.vote_info = vote_info
        self.ledger_commit_info = ledger_commit_info
        self.signatures = signatures
        self.author = author
        self.author_signature = str(author)

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
    def __init__(self,ledger_module):
        self.ledger_module = ledger_module
        
        self.pending_block_tree = TreeUtility()
        
        self.pending_votes={}
        qc = QC(
            VoteInfo(0,0,0,0,0),
            LedgerCommitInfo('str','str'),
            [],
            'str'
            )
        self.high_qc=qc
        self.high_commit_qc=qc

    """
    pending block tree; // tree of blocks pending commitment
    pending votes; // collected votes per block indexed by their LedgerInfo hash 
    high qc; // highest known QC
    high commit qc; // highest QC that serves as a commit certificate

    """
    
    def process_qc(self,qc):
        if qc.ledger_commit_info:
            ledger_state=self.ledger_module.commit(qc.vote_info.parent_id)
            self.pending_block_tree=self.pending_block_tree.prune(qc.vote_info.parent_id)
            self.high_commit_qc = max(qc.vote_info.round,self.high_commit_qc.vote_info.round)
        self.high_qc = max(qc.vote_info.round,self.high_qc.vote_info.round)

    """
    Procedure process qc(qc)
        if qc.ledger commit info.commit state id ̸= ⊥ then
        Ledger.commit(qc.vote info.parent id)
        pending block tree.prune(qc.vote info.parent id) // parent id becomes the new root of
        Pending
        high commit qc ← maxround {qc, high commit qc} high qc ← maxround{qc, high qc}

    """
    
    def execute_and_insert(self,b):
        id = self.ledger_module.speculate(b.qc.vote_info.id,b.id,b)
        #how to get parent id
        id = self.pending_block_tree.add(b,b.qc.vote_info.id)
        #print(id)

        

    
    def generate_block(self,txns,current_round,author):
        #where will author come from
        b = Block(author,current_round,txns,self.high_qc,uuid.uuid4())
        return b

    """
    Function generate block(txns, current round) 
        return Block ⟨
        author ← u,
        round ← current round,
        payload ← txns,
        qc ← high qc,
        id ← hash(author || round || payload || qc.vote info.id || qc.signatures) ⟩

    """

    def process_vote(self,v,f,author):
        self.process_qc(v.high_commit_qc)
        vote_idx = str(v.ledger_commit_info.commit_state_id)+str(v.ledger_commit_info.vote_info_hash)
        #if vote idx does not exist???
        if vote_idx not in self.pending_votes.keys():
            self.pending_votes[vote_idx]=[]
        self.pending_votes[vote_idx] = self.pending_votes[vote_idx] + [v.signature]
        if len(self.pending_votes[vote_idx]) == 2*f+1:
            commit_info = v.ledger_commit_info
            #str(v.ledger_commit_info.commit_state_id)+str(v.ledger_commit_info.vote_info_hash)
            #hash(v.ledger_commit_info)
            votes = self.pending_votes[vote_idx]

            #
            #where will author come from
            #
            return QC(v.vote_info,commit_info,votes,author)
        return None

        """
        Function process vote(v)
            process qc(v.high commit qc)
            vote idx ← hash(v.ledger commit info)
            pending votes[vote idx] ← pending votes[vote idx] ∪ v.signature 
            if |pending votes[vote idx]| = 2f + 1 then
            qc ←QC ⟨
                vote info ← v.vote info,
                state id ← v.state id,
                votes ← pending votes[vote idx] ⟩
            return qc
            return ⊥

        """

    

    