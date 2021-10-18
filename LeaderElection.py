
import math, random
class LeaderElection:
    def __init__(self,validator_list,window_size,exclude_size,ledger_module,pacemaker_module):
        self.ledger_module = ledger_module
        self.pacemaker_module=pacemaker_module
        self.validators = validator_list    #The list of current validators
        self.window_size = window_size    #A parameter for the leader reputation algorithm
        self.exclude_size = exclude_size    #Between f and 2f, number of excluded authors of last committed blocks reputation leaders; // Map from round numbers to leaders elected due to the reputation scheme
        self.reputation_leaders = []    #Map from round numbers to leaders elected due to the reputation scheme

    def elect_reputation_leader(self,qc):
        active_validators = [] # validators that signed the last window size committed blocks 
        last_authors = [] # ordered set of authors of last exclude size committed blocks 
        current_qc = qc
        i = 0
        while i<self.window_size or len(last_authors) < self.exclude_size:
            current_block = self.ledger_module.committed_block(current_qc.vote_info.parent_id)
            block_author = current_block.author
            if i < self.window_size:
                ########
                active_validators.append(current_qc.signatures.signers()) 
            if len(last_authors) < self.exclude_size :
                last_authors.append(block_author)
            current_qc = current_block.qc
        for x in last_authors:
            active_validators.remove(x)
        return active_validators[int(random.seed(current_qc.vote_info.round)*len(active_validators))]
        
    def update_leaders(self,qc):
        extended_round = qc.vote_info.parent_round
        qc_round = qc.vote_info.round
        current_round = self.pacemaker_module.current_round
        if extended_round + 1 == qc_round and qc_round + 1 == current_round :
            self.reputation_leaders[current_round + 1] = self.elect_reputation_leader(qc)
    
    def get_leader(self,round):
        if self.reputation_leaders[round]:
            return self.reputation_leaders[round]
        index =math.floor(round/2) % len(self.validators)
        return index