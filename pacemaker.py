class Pacemaker:
    def __init__(self,current_round,last_round_tc,pending_timeouts):
        self.current_round = current_round
        self.last_round_tc = last_round_tc
        self.pending_timeouts = pending_timeouts
    
    def get_round_timer(r):
        return #round timer formula

    def start_timer(new_round):
        ######
        stop_timer(current_round)
        current_round = new_round
        #start local timer for current_round for duration get_round_timer(current round)

    def local_timeout_round(self):
        #####
        save_consensus_state()
        #######
        timeout_info = safety.make_timeout(self.current_round,block_tree.high_qc,self.last_round_tc)
        #######
        broadcast TimeoutMsg (timeout_info,self.last_round_tc,block_tree.high_commit_qc)

    def process_remote_timeout_round(self,tmo):
        tmo_info = tmo.tmo_info
        if tmo_info.round < self.current_round:
            return None

        ###########
        if tmo_info.sender not in self.pending_timeouts[tmo_info.round].sender:
            self.pending_timeouts[tmo_info.round] = self.pending_timeouts[tmo_info.round] + [tmo_info]
        if len(self.pending_timeouts[tmo_info.round].sender)==f+1:
            stop_timer(self.current_round)
            self.local_timeout_round()
        if len(self.pending_timeouts[tmo_info.round].sender)==f2+1:
            t = TC(
                round=tmo_info.round,
                #########
                tmo_high_qc_rounds=,
                signatures=)
        return None

    def advance_round_tc(self,tc):
        if tc==None or tc.round < self.current_round:
            return False
        self.last_round_tc = tc
        self.start_timer(tc.round +1)
        return True

    def advance_round_qc(self,qc):
        if qc.vote_info.round < self.current_round:
            return False
        self.last_round_tc = None
        self.start_timer(qc.vote_info.round+1)
        return True 


        