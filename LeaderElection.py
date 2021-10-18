from ledger import Ledger
from pacemaker import Pacemaker
class LeaderElection:
    def __init__(self,validators,window_size,exclude_size,reputation_leaders):
        self.validators = validators     #The list of current validators
        self.window_size = window_size    #A parameter for the leader reputation algorithm
        self.exclude_size = exclude_size    #Between f and 2f, number of excluded authors of last committed blocks reputation leaders; // Map from round numbers to leaders elected due to the reputation scheme
        self.reputation_leaders = reputation_leaders    #Map from round numbers to leaders elected due to the reputation scheme

    def elect_reputation_leader(self,qc):
        active_validators = None # validators that signed the last window size committed blocks 
        last_authors = None # ordered set of authors of last exclude size committed blocks 
        current_qc = qc
        ####
        for i = 0; i < self.window_size or last_authors < self.exclude_size; i = i + 1):
            current_block = Ledger.committed_block(current_qc.vote_info.parent_id)
            block_author = current_block.author
            if i < self.window_size:
                #####
                active_validators = active_validators ∪ current_qc.signatures.signers() 
                # |current qc.signatures.signers()| ≥ 2f + 1
            if |last authors| < exclude_size :
                #####
                last_authors = last_authors ∪ {block_author}
            current_qc = current_block.qc    ####
        active_validators = active_validators \ last_authors 
        #contains at least 1 validator return active validators.pick one(seed ← qc.voteinfo.round)
    
    def update_leaders(self,qc):
        extended_round = qc.vote_info.parent_round
        qc_round = qc.vote_info.round
        current_round = PaceMaker.current_round
        if extended_round + 1 == qc_round and qc_round + 1 == current_round :
            reputation_leaders[current_round + 1] = elect_reputation_leader(qc)
    
    def get_leader(self,round):
         #######
        if ⟨round, leader⟩ ∈ reputation_leaders :
            return leader  #Reputation-based leader
            #####
        return validators[⌊round/2⌋ mod |validators|] # Round-robin leader (two rounds per leader)