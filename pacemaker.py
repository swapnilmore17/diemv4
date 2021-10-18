from ledger import Ledger
from blocktree import BlockTree
from datastructs import TimeoutMsg
from datastructs import TC
from safety import Safety

class Pacemaker:
    def __init__(self,current_round,last_round_tc,pending_timeouts):
        self.current_round = current_round
        self.last_round_tc = last_round_tc
        self.pending_timeouts = pending_timeouts
        self.run_done = False
        self.round_done = False
    
    def get_round_timer(r,delta):
        
        #round timer formula
        return 4 * delta

    def start_timer(self,new_round):
        ######
        #stop_timer(current_round)
        self.round_done=True
        #change the run_done value
        self.current_round = new_round

        
        """"""""""""""
        #start local timer for current_round for duration get_round_timer(current round)
    """"""
    def stop_timer(self,round):
        self.round_done=False

    def local_timeout_round(self):
        #####
        #save_consensus_state()
        #######
        timeout_info = Safety.make_timeout(self.current_round,BlockTree.high_qc,self.last_round_tc)
        #######
        return TimeoutMsg (timeout_info,self.last_round_tc, BlockTree.high_commit_qc)
        #broadcast from da file

    def process_remote_timeout_round(self,tmo,f):
        tmo_info = tmo.tmo_info
        if tmo_info.round < self.current_round:
            return None

        ###########
        sender_list = [x.sender for x in self.pending_timeouts[tmo_info.round]]

        if tmo_info.sender not in sender_list:
            self.pending_timeouts[tmo_info.round] = self.pending_timeouts[tmo_info.round] + [tmo_info]
        if len(sender_list)==f+1:
            """"""
            self.stop_timer(self.current_round)

            self.local_timeout_round()
        if len(sender_list)==f*2+1:
            t = TC(
                round=tmo_info.round,
                #########
                tmo_high_qc_rounds=[x.high_qc.vote_info.round for x in self.pending_timeouts[tmo_info.round]],
                signatures=[x.signature for x in self.pending_timeouts[tmo_info.round]])
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


        