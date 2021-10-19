
from datastructs import TimeoutMsg
from datastructs import TC


class Pacemaker:
    def __init__(self,current_round,last_round_tc,pending_timeouts,safety_module,block_tree_module):
        self.current_round = current_round
        self.last_round_tc = last_round_tc
        self.pending_timeouts = pending_timeouts
        self.run_done = False
        self.round_done = False
        self.delta = 10
        self.safety_module = safety_module
        self.block_tree_module = block_tree_module
    
    def get_round_timer(self,r):
        
        #round timer formula
        return 4 * self.delta

    def start_timer(self,new_round):
        ######
        #stop_timer(current_round)
        self.round_done=True
        #change the run_done value
        self.current_round = new_round
    
    """
    Procedure start timer(new round)
        stop timer(current round)
        current round ← new round
        start local timer for round current round for duration get round timer(current round)

    """

    def stop_timer(self,round):
        self.round_done=False

    def local_timeout_round(self):

        timeout_info = self.safety_module.make_timeout(self.current_round,self.block_tree_module.high_qc,self.last_round_tc)
        #######
        return TimeoutMsg (timeout_info,self.last_round_tc, self.block_tree_module.high_commit_qc)
        #broadcast from da file

    """
    Procedure local timeout round()
        save consensus state()
        timeout info ← Safety.make timeout(current round, Block-Tree.high qc, last round tc) 
        broadcast TimeoutMsg⟨timeout info, last round tc, Block-Tree.high commit qc⟩

    """

    def process_remote_timeout_round(self,tmo,f):
        tmo_info = tmo.tmo_info
        if tmo_info.round < self.current_round:
            return None

        ###########
        sender_list = [x.sender for x in self.pending_timeouts[tmo_info.round]]

        if tmo_info.sender not in sender_list:
            self.pending_timeouts[tmo_info.round] = self.pending_timeouts[tmo_info.round] + [tmo_info]
        if len(sender_list)==f+1:
            self.stop_timer(self.current_round)

            self.local_timeout_round()
        if len(sender_list)==f*2+1:
            t = TC(
                round=tmo_info.round,
                tmo_high_qc_rounds=[x.high_qc.vote_info.round for x in self.pending_timeouts[tmo_info.round]],
                signatures=[x.signature for x in self.pending_timeouts[tmo_info.round]])
        return None

    """
    Function process remote timeout(tmo) 
        tmo info ← tmo.tmo info
        if tmo info.round < current round then 
        return ⊥
        if tmo info.sender ̸∈ pending timeouts[tmo info.round].senders then
            pending timeouts[tmo info.round] ← pending timeouts[tmo info.round] ∪ {tmo info}
        if |pending timeouts[tmo info.round].senders| == f + 1 then 
            stop timer(current round)
            local timeout round() // Bracha timeout
        if |pending timeouts[tmo info.round].senders| == 2f + 1 then 
        return TC ⟨
            round ← tmo info.round,
            tmo high qc rounds ← {t.high qc.round | t ∈ pending timeouts[tmo info.round]}, 
            signatures ← {t.signature | t ∈ pending timeouts[tmo info.round]}⟩)
        return ⊥

    """

    def advance_round_tc(self,tc):
        if tc==None or tc.round < self.current_round:
            return False
        self.last_round_tc = tc
        self.start_timer(tc.round +1)
        return True

    """
    Function advance round tc(tc)
        if tc = ⊥ ∨ tc.round < current round then
        return false 
        last round tc ← tc
        start timer(tc.round + 1) 
        return true

    """

    def advance_round_qc(self,qc):
        if qc.vote_info.round < self.current_round:
            return False
        self.last_round_tc = None
        self.start_timer(qc.vote_info.round+1)
        return True 
        
    """
    Function advance round qc(qc)
        if qc.vote info.round < current round then
        return false
        last round tc ← ⊥
        start timer(qc.vote info.round + 1) 
        return true

    """

        