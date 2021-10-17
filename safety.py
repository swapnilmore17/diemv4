class Safety:
    def __init__(self,private_key,public_keys,highest_vote_round,highest_qc_round):
        self.private_key = private_key # Own private key
        self.public_keys = public_keys # Public keys of all validators 
        self.highest_vote_round = highest_vote_round # initially 0
        self.highest_qc_round = highest_qc_round

    def increase_highest_vote_round(self,round):
        # commit not to vote in rounds lower than round
        self.highest_vote_round = max(round, self.highest_vote_round)

    def update_highest_qc_round(self,qc_round):
        self.highest_qc_round = max(qc_round, self.highest_qc_round)

    def consecutive(self,block_round, round):
        return round + 1 = block_round    ##########

    def safe_to_extend(self,block_round, qc_round, tc):
        return consecutive(block_round, tc.round) and qc_round >= max(tc.tmo_high_qc_rounds)

    def safe_to_vote(self,block_round, qc_round, tc):
        if block_round <= max(self.highest_vote_round, qc_round):
             # 1. must vote in monotonically increasing rounds // 2. must extend a smaller round
            return False
            # Extending qc from previous round or safe to extend due to tc
        return consecutive(block_round, qc_round) or safe_to_extend(block_round, qc_round, tc)

    def safe_to_timeout(self,round, qc_round, tc):
        if qc_round < self.highest_qc_round or round <= max(self.highest_vote_round − 1, qc_round) :  ########
            # respect highest qc round and don’t timeout in a past round
            return False
        # qc or tc must allow entering the round to timeout
        return consecutive(round, qc_round) or consecutive(round, tc.round)

    def commit_state_id_candidate(self,block_round, qc):
        # find the committed id in case a qc is formed in the vote round if consecutive(block round, qc.vote info.round) then
        if consecutive(block_round, qc.vote_info.round):
            return Ledger.pending_state(qc.id) 
        else:
            return None
