class Safetypublic: 
    def make_vote(self,b, last_tc):
        qc_round = b.qc.vote_info.round
        if valid_signatures(b, last_tc) and safe_to_vote(b.round, qc_round, last_tc):
            update_highest_qc_round(qc_round) # Protect qc round
            increase_highest_vote_round(b.round) # Don’t vote again in this (or lower) round
            #VoteInfo carries the potential QC info with ids and rounds of the parent QC
            
            vote_info = VoteInfo(   ########
                id = b.id
                round =  b.round
                parent_id, parent_round = b.qc.vote_info.id, qc_round) 
                exec_state_id = Ledger.pending_state(b.id) )

            ledger_commit_info = LedgerCommitInfo (  #######
                commit_state_id = commit_state_id_candidate(b.round, b.qc), 
                vote_info_hash = hash(vote_info) )

            return VoteMsg(vote_info, ledger_commit_info, BlockTree.high_commit_qc) 
        return None
        
    def make_timeout(self,round, high_qc, last_tc):
        qc_round = high_qc.vote_info.round
        if valid_signatures(high_qc, last_tc) and safe_to_timeout(round, qc_round, last_tc):
            increase_highest_vote_round(round) # Stop voting for round
            return TimeoutInfo(round, high_qc)
        return None